import openai
import requests
import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class ImageGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        openai.api_key = self.openai_api_key
        self.model = "dall-e-3"
        self.size = "1024x1024"
        self.quality = "standard"
    
    def load_general_prompt(self):
        """Load the general image generation prompt"""
        prompt_path = Path("prompts/image_generation/common_prompt.txt")
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def load_platform_prompt(self, platform):
        """Load platform-specific image generation prompt"""
        prompt_path = Path(f"prompts/image_generation/{platform}.txt")
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def generate_media_prompt(self, social_media_content, full_post_content, image_generation_prompt):
        """Generate a media prompt by combining all three inputs: image generation guidelines, full post content, and social media content"""
        try:
            # Use system role for instructions and user role for content
            system_message = image_generation_prompt
            
            user_message = f"""**FULL BLOG POST CONTENT:**
{full_post_content}

**SOCIAL MEDIA CONTENT:**
{social_media_content}

Based on the guidelines provided in the system message, create a detailed media_prompt for image generation that combines insights from both the full blog post and social media content."""

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating media prompt: {e}")
            return None
    
    def move_to_media_history(self, version_path):
        """Move existing media files to media_history before generating new ones"""
        version_path = Path(version_path)
        media_dir = version_path / "media"
        media_history_dir = version_path / "media_history"
        
        # Check if media directory exists and has files
        if not media_dir.exists():
            return True
        
        # Get list of existing media files
        media_files = list(media_dir.glob("*"))
        if not media_files:
            return True
        
        # Create media_history directory if it doesn't exist
        media_history_dir.mkdir(exist_ok=True)
        
        # Generate timestamp for this backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            for media_file in media_files:
                if media_file.is_file():
                    # Create timestamped filename
                    file_extension = media_file.suffix
                    base_name = media_file.stem
                    history_filename = f"{base_name}_{timestamp}{file_extension}"
                    history_path = media_history_dir / history_filename
                    
                    # Move file to history
                    shutil.move(str(media_file), str(history_path))
                    print(f"Moved {media_file.name} to media_history as {history_filename}")
            
            return True
            
        except Exception as e:
            print(f"Error moving files to media_history: {e}")
            return False
    
    def generate_image(self, prompt, output_path):
        """Generate an image from a prompt and save it"""
        try:
            response = openai.images.generate(
                model=self.model,
                prompt=prompt,
                size=self.size,
                quality=self.quality,
                n=1,
            )
            image_url = response.data[0].url
            
            # Download and save the image
            image_data = requests.get(image_url).content
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(image_data)
            
            print(f"Image successfully saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating/saving image: {e}")
            return None
    
    def process_social_media_version(self, version_path, regenerate_mode=False):
        """Process a single version directory to generate media prompt and image"""
        version_path = Path(version_path)
        content_file = version_path / "content.txt"
        
        if not content_file.exists():
            print(f"No content.txt found in {version_path}")
            return False
        
        # Read social media content
        with open(content_file, 'r', encoding='utf-8') as f:
            social_media_content = f.read()
        
        # Extract post name from path to find the corresponding blog post
        post_name = version_path.parts[-3]  # e.g., "2019-06-15-visit-a-tea-shop-to-gift-feedback"
        blog_post_path = Path("_posts") / f"{post_name}.md"
        
        # Read full blog post content
        full_post_content = ""
        if blog_post_path.exists():
            with open(blog_post_path, 'r', encoding='utf-8') as f:
                full_post_content = f.read()
        else:
            print(f"Warning: Blog post not found at {blog_post_path}")
        
        # Extract platform from path
        platform = version_path.parts[-2]  # e.g., "Resend", "X", "LinkedIn"
        
        if platform in ["Resend","TikTok"]:
            print(f"Skipping platform {platform} as it is not supported for image generation")
            return False

        # Handle media prompt based on mode
        media_prompt_file = version_path / "media_prompt.txt"
        
        if regenerate_mode and media_prompt_file.exists():
            # Regeneration mode: use existing media prompt
            with open(media_prompt_file, 'r', encoding='utf-8') as f:
                media_prompt = f.read().strip()
            print(f"Regeneration mode: Using existing media prompt from: {media_prompt_file}")
        else:
            # Normal mode: generate new media prompt
            # Load both general and platform-specific prompts
            general_prompt = self.load_general_prompt()
            platform_prompt = self.load_platform_prompt(platform)
            
            # Combine prompts
            combined_prompt = general_prompt
            if platform_prompt:
                combined_prompt += f"\n\n## Platform-Specific Guidelines for {platform}\n{platform_prompt}"
            
            # Generate media prompt using all inputs including platform-specific guidelines
            media_prompt = self.generate_media_prompt(social_media_content, full_post_content, combined_prompt)
            if not media_prompt:
                return False
            
            # Save media prompt
            with open(media_prompt_file, 'w', encoding='utf-8') as f:
                f.write(media_prompt)
            print(f"Media prompt generated and saved to: {media_prompt_file}")
        
        # Move existing media files to history before generating new ones
        if not self.move_to_media_history(version_path):
            print(f"Warning: Failed to move existing media to history for {version_path}")
        
        # Create media directory and generate image
        media_dir = version_path / "media"
        media_dir.mkdir(exist_ok=True)
        
        image_path = media_dir / "generated_image.png"
        generated_image = self.generate_image(media_prompt, str(image_path))
        
        return generated_image is not None
    
    def process_all_versions(self, base_path="social_media", regenerate_mode=False):
        """Process all social media versions to generate media prompts and images"""
        base_path = Path(base_path)
        if not base_path.exists():
            print(f"Base path {base_path} does not exist")
            return
        
        processed_count = 0
        
        # Walk through all directories
        for post_dir in base_path.iterdir():
            if not post_dir.is_dir():
                continue
            
            print(f"\nProcessing post: {post_dir.name}")
            
            # Process each platform
            for platform_dir in post_dir.iterdir():
                if not platform_dir.is_dir():
                    continue
                
                print(f"  Processing platform: {platform_dir.name}")
                
                # Process each version
                for version_dir in platform_dir.iterdir():
                    if not version_dir.is_dir() or not version_dir.name.startswith('v'):
                        continue
                    
                    print(f"    Processing version: {version_dir.name}")
                    
                    if self.process_social_media_version(version_dir, regenerate_mode):
                        processed_count += 1
                        print(f"    ✓ Successfully processed {version_dir}")
                    else:
                        print(f"    ✗ Failed to process {version_dir}")
        
        print(f"\nProcessed {processed_count} versions total")
    
    def regenerate_for_changed_prompts(self, base_path="social_media"):
        """Regenerate images for versions where prompts have changed"""
        # This would typically be called by a git hook or CI/CD pipeline
        # For now, it processes all versions
        self.process_all_versions(base_path, regenerate_mode=True)

def main():
    """Main function to run the image generator"""
    import sys
    
    try:
        generator = ImageGenerator()
        
        if len(sys.argv) < 2:
            print("Usage:")
            print("  python image_generation.py <version_path>")
            print("  python image_generation.py <version_path> --regenerate")
            print("  python image_generation.py --all")
            print("")
            print("Examples:")
            print("  python image_generation.py social_media/2019-06-15-visit-a-tea-shop-to-gift-feedback/Resend/v1")
            print("  python image_generation.py social_media/2019-06-15-visit-a-tea-shop-to-gift-feedback/Resend/v1 --regenerate")
            print("  python image_generation.py --all")
            return
        
        # Check for regenerate flag
        regenerate_mode = "--regenerate" in sys.argv
        
        if sys.argv[1] == "--all":
            # Process all existing social media versions
            generator.process_all_versions(regenerate_mode=regenerate_mode)
        else:
            # Process single version
            version_path = sys.argv[1]
            if generator.process_social_media_version(version_path, regenerate_mode):
                print(f"✓ Successfully processed {version_path}")
            else:
                print(f"✗ Failed to process {version_path}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
