"""
Post content to social media platforms.

This script posts content from the social_media directory to social media platforms.
It can be run in two modes:
1. Post content from a specific folder: python post_social_media.py social_media/folder_name
2. Post content from all folders: python post_social_media.py social_media

The script automatically detects the platforms from the subfolders in each folder.
"""
import os
import sys
from pathlib import Path

from posting import SocialMediaPoster


def post_content(folder_path: str, output_path: str = "posting_results.json") -> None:
    """
    Post content from a folder or all folders to social media platforms.
    
    Args:
        folder_path: Path to the folder containing platform folders or the base directory
        output_path: Path to save the posting results
    """
    folder_path = Path(folder_path)
    
    # Create poster
    poster = SocialMediaPoster(output_path)
    
    # Check if folder is the social_media directory (post from all folders)
    if folder_path.name == "social_media":
        # Get all page folders
        page_folders = [p for p in folder_path.iterdir() if p.is_dir()]
        
        # Post from each folder
        all_results = []
        for folder in page_folders:
            # Handle folder names with spaces by using the string representation
            folder_str = str(folder)
            print(f"\nProcessing folder: {folder_str}")
            results = poster.post_from_folder(folder_str)
            all_results.extend(results)
        
        # Print summary
        if all_results:
            success_count = sum(1 for r in all_results if r.get("status") == "success")
            print(f"\n✅ Posted {success_count}/{len(all_results)} items")
            print(f"✅ Results saved to {output_path}")
    else:
        # Post from specific folder
        # Handle folder names with spaces by using the string representation
        folder_str = str(folder_path)
        print(f"\nProcessing folder: {folder_str}")
        results = poster.post_from_folder(folder_str)
        
        # Print summary
        if results:
            success_count = sum(1 for r in results if r.get("status") == "success")
            print(f"\n✅ Posted {success_count}/{len(results)} items")
            print(f"✅ Results saved to {output_path}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python post_social_media.py <folder_path> [output_file]")
        sys.exit(1)
    
    # Get folder path
    folder_path = sys.argv[1]
    
    # Default output file
    output_file = "posting_results.json"
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        sys.exit(1)
    
    # Check if folder is a directory
    if not os.path.isdir(folder_path):
        print(f"Not a directory: {folder_path}")
        sys.exit(1)
    
    # Post content
    post_content(folder_path, output_file)


if __name__ == "__main__":
    main()
