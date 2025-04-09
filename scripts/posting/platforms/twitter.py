"""
Twitter (X) platform implementation using Tweepy API v2
"""
import os
import glob
import tweepy
from typing import Dict, Any, List
from pathlib import Path

from ..platforms import SocialMediaPlatform

class TwitterPlatform(SocialMediaPlatform):
    """Twitter (X) platform implementation using API v2."""
    
    def __init__(self):
        super().__init__("X")
        self._verify_credentials()
    
    def _verify_credentials(self):
        required_creds = [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
            "TWITTER_ACCESS_TOKEN", 
            "TWITTER_ACCESS_SECRET"
        ]
        missing = [cred for cred in required_creds if not os.getenv(cred)]
        if missing:
            raise ValueError(f"Missing credentials: {', '.join(missing)}")
    
    def get_client(self) -> tweepy.Client:
        """Initialize and return Twitter v2 API client."""
        return tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
        )
    
    def get_auth(self) -> tweepy.OAuth1UserHandler:
        """Initialize and return Twitter OAuth1 handler for v1.1 API."""
        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        return auth
    
    def get_api(self) -> tweepy.API:
        """Initialize and return Twitter v1.1 API."""
        auth = self.get_auth()
        return tweepy.API(auth)

    def find_media_files(self, platform_folder: str) -> List[str]:
        """
        Find media files in the platform folder.
        
        Args:
            platform_folder: Path to the platform folder
            
        Returns:
            List of media file paths
        """
        # Get the directory containing the content.txt file
        folder = os.path.dirname(platform_folder) if os.path.isfile(platform_folder) else platform_folder
        
        # Find all media files (images, videos)
        image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        video_extensions = ['mp4', 'mov', 'avi']
        
        media_files = []
        
        # Find image files
        for ext in image_extensions:
            media_files.extend(glob.glob(os.path.join(folder, f"*.{ext}")))
        
        # Find video files
        for ext in video_extensions:
            media_files.extend(glob.glob(os.path.join(folder, f"*.{ext}")))
        
        return media_files

    def post_content(self, content: str, page_name: str, platform_folder: str = None) -> Dict[str, Any]:
        """
        Post content to Twitter using API v2.
        
        Args:
            content: The content to post
            page_name: The name of the page
            platform_folder: Path to the platform folder (for finding media)
            
        Returns:
            Dict containing the result of the posting operation
        """
        try:
            # Find media files if platform_folder is provided
            media_ids = []
            if platform_folder:
                media_files = self.find_media_files(platform_folder)
                
                if media_files:
                    # Upload media using v1.1 API
                    api = self.get_api()
                    
                    for media_file in media_files:
                        print(f"Uploading media: {media_file}")
                        media = api.media_upload(media_file)
                        media_ids.append(media.media_id)
            
            # Post tweet with or without media
            client = self.get_client()
            
            if media_ids:
                response = client.create_tweet(text=content, media_ids=media_ids)
            else:
                response = client.create_tweet(text=content)
                
            tweet_id = response.data['id']
            
            user_info = client.get_me(user_auth=True)
            username = user_info.data.username

            tweet_url = f"https://x.com/{username}/status/{tweet_id}"
            return self.create_success_result(page_name, content, tweet_id, tweet_url)
            
        except tweepy.TweepyException as e:
            error_msg = f"Twitter API Error: {str(e)}"
            return self.create_error_result(page_name, content, error_msg)
