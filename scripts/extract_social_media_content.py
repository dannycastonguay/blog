import sys
import os
from pathlib import Path
import yaml
from openai import OpenAI

# Import the SocialMediaPoster to get available platforms
from posting import SocialMediaPoster

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

def extract_markdown_content(filepath):
    """
    Extract front matter and content from a markdown file.
    
    Args:
        filepath: Path to the markdown file
        
    Returns:
        Tuple of (front_matter, content)
    """
    with open(filepath, 'r') as f:
        content = f.read()
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = yaml.safe_load(parts[1])
            # Return raw markdown content instead of converting to HTML
            markdown_content = parts[2].strip()
            return front_matter, markdown_content
        else:
            return {}, content

def get_prompt_for_platform(platform, content):
    """
    Get the prompt for a platform from a file.
    
    Args:
        platform: Platform name
        content: Content to include in the prompt
        
    Returns:
        str: Prompt for the platform
    """
    # Check if a prompt file exists for this platform
    prompt_file = os.path.join("prompts", f"{platform}.txt")
    
    if os.path.exists(prompt_file):
        # Read prompt from file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        # Replace {content} placeholder with actual content
        prompt = prompt_template.replace("{content}", content)
    else:
        # Use default prompt if no file exists
        prompt = f"""
        Summarize the following blog post into an engaging {platform} post.
        
        Blog Post:
        {content}
        
        {platform} post:
        """
    
    return prompt

def generate_social_media_content(content, platform):
    # Get prompt for this platform
    prompt = get_prompt_for_platform(platform, content)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7
    )

    summary = response.choices[0].message.content.strip()
    return summary

def get_page_name(filepath):
    # Extract the filename without extension
    filename = os.path.basename(filepath)
    page_name = os.path.splitext(filename)[0]
    
    # Remove the date prefix if it exists (YYYY-MM-DD-)
    if len(page_name) > 11 and page_name[4] == '-' and page_name[7] == '-' and page_name[10] == '-':
        page_name = page_name[11:]
    
    return page_name

def save_social_media_content(page_name, platform, content):
    # Create directory structure if it doesn't exist
    directory = os.path.join("social_media", page_name, platform)
    os.makedirs(directory, exist_ok=True)
    
    # Save content to file
    filepath = os.path.join(directory, "content.txt")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def get_available_platforms():
    """
    Get available platforms from the SocialMediaPoster.
    
    Returns:
        List of platform names
    """
    # Create a temporary poster to get available platforms
    platforms = SocialMediaPoster.get_platforms(keys_only=True)
    return platforms

def process_page(filepath, platforms=None):
    """
    Process a page and generate social media content for each platform.
    
    Args:
        filepath: Path to the markdown file
        platforms: List of platforms to generate content for (default: all available platforms)
        
    Returns:
        Dict of platform to output path
    """
    if platforms is None:
        # Get all available platforms
        platforms = get_available_platforms()
    
    # Extract content from markdown file
    front_matter, content = extract_markdown_content(filepath)
    
    # Get page name
    page_name = get_page_name(filepath)
    
    results = {}
    
    # Generate and save content for each platform
    for platform in platforms:
        social_content = generate_social_media_content(content, platform)
        output_path = save_social_media_content(page_name, platform, social_content)
        results[platform] = output_path
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_social_media_content.py <markdown_file> [platform1,platform2,...]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Check if specific platforms are requested
    platforms = None
    if len(sys.argv) > 2:
        platforms = sys.argv[2].split(',')
    
    # Process the page
    results = process_page(filepath, platforms)
    
    # Print results
    for platform, path in results.items():
        print(f"✅ {platform} content saved to {path}")
