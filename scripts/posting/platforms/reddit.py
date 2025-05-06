"""
Reddit platform implementation (placeholder)
"""

import os
import glob
from typing import Dict, Any, List
from pathlib import Path

from ..platforms import SocialMediaPlatform


class RedditPlatform(SocialMediaPlatform):
    """Reddit platform implementation (placeholder)."""

    def __init__(self):
        super().__init__("Reddit")
        self._verify_credentials()

    def _verify_credentials(self):
        required_creds = [
            "REDDIT_CLIENT_ID",
            "REDDIT_CLIENT_SECRET",
            "REDDIT_USERNAME",
            "REDDIT_PASSWORD",
        ]
        missing = [cred for cred in required_creds if not os.getenv(cred)]
        if missing:
            raise ValueError(f"Missing credentials: {', '.join(missing)}")

    def find_media_files(self, platform_folder: str) -> List[str]:
        """
        Find media files in the platform folder.

        Args:
            platform_folder: Path to the platform folder

        Returns:
            List of media file paths
        """
        folder = (
            os.path.dirname(platform_folder)
            if os.path.isfile(platform_folder)
            else platform_folder
        )

        # Supported media extensions
        image_extensions = ["jpg", "jpeg", "png", "gif"]
        video_extensions = ["mp4", "mov", "webm"]

        media_files = []

        # Find files in current folder
        for ext in image_extensions + video_extensions:
            media_files.extend(glob.glob(os.path.join(folder, f"*.{ext}")))

        # Check parent folder if in version folder
        parent_folder = Path(folder).parent
        if Path(folder).name.startswith("v") and parent_folder.exists():
            for ext in image_extensions + video_extensions:
                media_files.extend(glob.glob(os.path.join(parent_folder, f"*.{ext}")))

        return media_files

    def post_content(
        self, content: str, page_name: str, platform_folder: str = None
    ) -> Dict[str, Any]:
        """
        Post content to Reddit (placeholder implementation).

        Args:
            content: The content to post
            page_name: The name of the page (used as post title)
            platform_folder: Path to the platform folder (for finding media)

        Returns:
            Dict containing the result of the posting operation
        """
        try:
            # Find media files if platform_folder is provided
            media_files = []
            if platform_folder:
                media_files = self.find_media_files(platform_folder)

            # PLACEHOLDER: In a real implementation, this would use the Reddit API
            # to post the content and media files

            # For now, just log what would be posted
            print(f"[PLACEHOLDER] Would post to Reddit:")
            print(f"Title: {page_name}")
            print(f"Content: {content}")

            if media_files:
                print(f"Media files: {', '.join(media_files)}")

            # Get subreddit from environment variable or use default
            subreddit = os.getenv("REDDIT_SUBREDDIT", "placeholder_subreddit")

            # Create a mock post ID and URL
            mock_post_id = "reddit_mock_id"
            mock_url = f"https://www.reddit.com/r/{subreddit}/comments/{mock_post_id}/placeholder_title"

            # Return success result with mock data
            return self.create_success_result(
                page_name, content, mock_post_id, mock_url
            )

        except Exception as e:
            error_msg = f"Reddit API Error: {str(e)}"
            return self.create_error_result(page_name, content, error_msg)
