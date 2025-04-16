import os
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional

def run_command(command):
    """
    Run a shell command and return the output
    
    Args:
        command: Command to run
    
    Returns:
        str: Command output
    """
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"Error running command: {command}")
        return ""
    return process.stdout.strip()

def get_git_references(base_ref=None, head_ref=None):
    """
    Get Git references for comparison
    
    Args:
        base_ref: Base Git reference (default: previous commit)
        head_ref: Head Git reference (default: current commit)
    
    Returns:
        tuple: (base_ref, head_ref)
    """
    if not head_ref:
        head_ref = run_command("git rev-parse HEAD")
    if not base_ref:
        base_ref = run_command(f"git rev-parse {head_ref}~1")
    
    return base_ref, head_ref

def get_changed_files_from_git(base_ref, head_ref):
    """
    Get files changed between two Git references using git diff
    
    Args:
        base_ref: Base Git reference
        head_ref: Head Git reference
    
    Returns:
        dict: Dictionary with lists of added, modified, and deleted files
    """
    # Get all changed files with status
    command = f"git diff --name-status {base_ref} {head_ref}"
    output = run_command(command)
    
    if not output:
        return {"added": [], "modified": [], "deleted": []}
    
    # Parse the output to categorize files
    added_files = []
    modified_files = []
    deleted_files = []
    
    for line in output.split("\n"):
        if not line.strip():
            continue
            
        # Split by tabs (git diff --name-status uses tab as separator)
        parts = line.split("\t")
        if len(parts) < 2:
            continue
            
        status = parts[0]
        
        if status.startswith("R"):  # Renamed
            # For renamed files, parts[1] is the old path and parts[2] is the new path
            if len(parts) >= 3:
                old_path = parts[1]
                new_path = parts[2]
                # Treat renamed files as a combination of deleted and added
                deleted_files.append(old_path)
                added_files.append(new_path)
            continue
            
        file_path = parts[1]
        
        if status.startswith("A"):  # Added
            added_files.append(file_path)
        elif status.startswith("M"):  # Modified
            modified_files.append(file_path)
        elif status.startswith("D"):  # Deleted
            deleted_files.append(file_path)
    
    return {
        "added": added_files,
        "modified": modified_files,
        "deleted": deleted_files
    }

def get_changed_files_from_pr():
    """
    Get files changed in a PR using GitHub CLI
    
    Returns:
        dict: Dictionary with lists of added, modified, and deleted files
    """
    # Get PR number from environment variable
    pr_number = os.getenv("PR_NUMBER")
    if not pr_number:
        print("PR_NUMBER environment variable not set")
        return {"added": [], "modified": [], "deleted": []}
    
    # Get the base commit SHA of the PR
    base_sha = run_command(f"gh pr view {pr_number} --json baseRefOid --jq '.baseRefOid'")
    if not base_sha:
        return {"added": [], "modified": [], "deleted": []}
    
    # Get all files in the PR
    command = f"gh pr view {pr_number} --json files --jq '.files[] | [.path, .additions, .deletions, .status] | @tsv'"
    output = run_command(command)
    
    if not output:
        return {"added": [], "modified": [], "deleted": []}
    
    # Parse the output to categorize files
    added_files = []
    modified_files = []
    deleted_files = []
    
    for line in output.split("\n"):
        if not line.strip():
            continue
            
        parts = line.split("\t")
        if len(parts) < 3:
            continue
            
        file_path = parts[0]
        additions = int(parts[1])
        deletions = int(parts[2])
        status = parts[3] if len(parts) > 3 else ""
        
        # Handle renamed files (if status is available)
        if status == "renamed":
            # For renamed files, treat them as new files
            added_files.append(file_path)
            continue
        
        # Check if the file existed in the base commit
        check_command = f"git cat-file -e {base_sha}:{file_path} 2>/dev/null || echo 'not_exists'"
        result = run_command(check_command)
        
        if result == 'not_exists':
            # File didn't exist in base commit, so it's new
            added_files.append(file_path)
        elif deletions == 0 and additions > 0:
            # File existed and only has additions
            modified_files.append(file_path)
        elif additions == 0 and deletions > 0:
            # File existed and only has deletions
            deleted_files.append(file_path)
        else:
            # File has both additions and deletions
            modified_files.append(file_path)
    
    return {
        "added": added_files,
        "modified": modified_files,
        "deleted": deleted_files
    }

def filter_posts(files, posts_dir="_posts"):
    """
    Filter files to only include posts
    
    Args:
        files: List of files
        posts_dir: Directory containing posts
    
    Returns:
        list: List of page files
    """
    # Pattern to match page files (e.g., _posts/YYYY-MM-DD-title.md)
    page_pattern = re.compile(f"^{posts_dir}/.*\\.md$")
    
    # Filter files that match the pattern
    return [f for f in files if page_pattern.match(f)]

def detect_changed_posts(base_ref=None, head_ref=None, posts_dir="_posts", pr_mode=False):
    """
    Detect changed posts (new, modified, deleted) between two Git references or in a PR
    
    Args:
        base_ref: Base Git reference (default: previous commit)
        head_ref: Head Git reference (default: current commit)
        posts_dir: Directory containing posts
        pr_mode: Whether to use PR mode (default: False)
    
    Returns:
        dict: Dictionary with lists of added, modified, and deleted posts
    """
    # Get changed files based on mode
    if pr_mode:
        changed_files = get_changed_files_from_pr()
    else:
        # Get Git references
        base_ref, head_ref = get_git_references(base_ref, head_ref)
        changed_files = get_changed_files_from_git(base_ref, head_ref)
    
    # Filter to only include posts
    new_posts = filter_posts(changed_files["added"], posts_dir)
    modified_posts = filter_posts(changed_files["modified"], posts_dir)
    deleted_posts = filter_posts(changed_files["deleted"], posts_dir)
    
    # Count total changes
    total_changes = len(new_posts) + len(modified_posts) + len(deleted_posts)
    
    if total_changes > 0:
        print(f"Found {total_changes} changed posts:")
        print(f"  - {len(new_posts)} new posts")
        print(f"  - {len(modified_posts)} modified posts")
        print(f"  - {len(deleted_posts)} deleted posts")
    else:
        print("No changed posts detected")
    
    return {
        "added": new_posts,
        "modified": modified_posts,
        "deleted": deleted_posts
    }

if __name__ == "__main__":
    # Parse command line arguments
    base_ref = None
    head_ref = None
    posts_dir = "_posts"
    pr_mode = False
    
    # Check for --pr-mode flag
    if "--pr-mode" in sys.argv:
        pr_mode = True
        sys.argv.remove("--pr-mode")
    
    if len(sys.argv) > 1:
        base_ref = sys.argv[1]
    if len(sys.argv) > 2:
        head_ref = sys.argv[2]
    if len(sys.argv) > 3:
        posts_dir = sys.argv[3]
    
    # Detect changed posts
    changed_posts = detect_changed_posts(base_ref, head_ref, posts_dir, pr_mode)
    
    # Print changed posts
    if any(changed_posts.values()):
        # Print new posts
        if changed_posts["added"]:
            print("\nNew posts:")
            for page in changed_posts["added"]:
                print(f"  + {page}")
        
        # Print modified posts
        if changed_posts["modified"]:
            print("\nModified posts:")
            for page in changed_posts["modified"]:
                print(f"  ~ {page}")
        
        # Print deleted posts
        if changed_posts["deleted"]:
            print("\nDeleted posts:")
            for page in changed_posts["deleted"]:
                print(f"  - {page}")
        
        # Output for GitHub Actions if GITHUB_OUTPUT is set
        if 'GITHUB_OUTPUT' in os.environ:
            import json
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                # Output new posts as JSON array
                f.write(f"new_posts={json.dumps(changed_posts['added'])}\n")
                
                # Output modified posts as JSON array
                f.write(f"modified_posts={json.dumps(changed_posts['modified'])}\n")
                
                # Output deleted posts as JSON array
                f.write(f"deleted_posts={json.dumps(changed_posts['deleted'])}\n")
                
                # Output all changed posts as JSON array
                all_changed = changed_posts["added"] + changed_posts["modified"] + changed_posts["deleted"]
                f.write(f"changed_posts={json.dumps(all_changed)}\n")
    else:
        print("No changed posts detected")
        if 'GITHUB_OUTPUT' in os.environ:
            import json
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                # Output empty arrays for all outputs
                f.write(f"new_posts={json.dumps([])}\n")
                f.write(f"modified_posts={json.dumps([])}\n")
                f.write(f"deleted_posts={json.dumps([])}\n")
                f.write(f"changed_posts={json.dumps([])}\n")
