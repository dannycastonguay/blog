"""
TikTok platform implementation (placeholder)

TikTok is a video-sharing platform that focuses on short-form video content.
This implementation handles the creation and posting of TikTok videos with captions.
"""

import os
import glob
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..platforms import SocialMediaPlatform


class TikTokPlatform(SocialMediaPlatform):
    """TikTok platform implementation for short-form video content."""

    def __init__(self):
        super().__init__("TikTok")
        self._verify_credentials()

    def _verify_credentials(self):
        required_creds = ["TIKTOK_ACCESS_TOKEN"]
        missing = [cred for cred in required_creds if not os.getenv(cred)]
        if missing:
            raise ValueError(f"Missing credentials: {', '.join(missing)}")

    def find_media_files(self, platform_folder: str) -> Dict[str, List[str]]:
        """
        Find video files in the platform folder.

        Args:
            platform_folder: Path to the platform folder

        Returns:
            Dict containing lists of video files
        """
        folder = (
            os.path.dirname(platform_folder)
            if os.path.isfile(platform_folder)
            else platform_folder
        )

        # TikTok only supports video content
        video_extensions = ["mp4", "mov", "webm"]

        # Audio files that might be used for TikTok videos
        audio_extensions = ["mp3", "wav", "m4a"]

        videos = []
        audio_files = []

        # Find files in current folder
        for ext in video_extensions:
            videos.extend(glob.glob(os.path.join(folder, f"*.{ext}")))

        for ext in audio_extensions:
            audio_files.extend(glob.glob(os.path.join(folder, f"*.{ext}")))

        # Check parent folder if in version folder
        parent_folder = Path(folder).parent
        if Path(folder).name.startswith("v") and parent_folder.exists():
            for ext in video_extensions:
                videos.extend(glob.glob(os.path.join(parent_folder, f"*.{ext}")))

            for ext in audio_extensions:
                audio_files.extend(glob.glob(os.path.join(parent_folder, f"*.{ext}")))

        return {"videos": videos, "audio": audio_files}

    def post_content(
        self, content: str, page_name: str, platform_folder: str = None
    ) -> Dict[str, Any]:
        """
        Post video content to TikTok (placeholder implementation).

        Args:
            content: The script/caption for the TikTok video
            page_name: The name of the page
            platform_folder: Path to the platform folder (for finding media)

        Returns:
            Dict containing the result of the posting operation
        """
        try:
            # Find media files if platform_folder is provided
            media_files = {"videos": [], "audio": []}
            if platform_folder:
                media_files = self.find_media_files(platform_folder)

            # TikTok requires video content
            if not media_files["videos"]:
                # Instead of raising an error, return a more helpful message
                # about what's needed to create a TikTok post
                return self.create_error_result(
                    page_name,
                    content,
                    "TikTok posts require video content. Please provide a video file (mp4, mov, or webm).",
                )

            # Extract script sections from content if it follows the timing format
            script_sections = self._parse_tiktok_script(content)

            # PLACEHOLDER: In a real implementation, this would use the TikTok API
            # to post the video with caption and possibly use the script sections
            # for video editing/captioning

            # For now, just log what would be posted
            print(f"[PLACEHOLDER] Would post to TikTok:")
            print(f"Video: {media_files['videos'][0]}")

            if script_sections:
                print(f"Script sections: {len(script_sections)} timing segments")
                for timing, text in script_sections:
                    print(f"  {timing}: {text[:30]}...")
            else:
                print(f"Caption: {content[:50]}...")

            if media_files["audio"]:
                print(f"Audio track: {media_files['audio'][0]}")

            # Create a mock post ID and URL
            mock_post_id = "tiktok_mock_id"
            mock_url = "https://www.tiktok.com/@user/video/placeholder"

            # Return success result with mock data
            return self.create_success_result(
                page_name, content, mock_post_id, mock_url
            )

        except Exception as e:
            error_msg = f"TikTok API Error: {str(e)}"
            return self.create_error_result(page_name, content, error_msg)

    def _parse_tiktok_script(self, content: str) -> Optional[List[tuple]]:
        """
        Parse a TikTok script with timing indicators.

        Args:
            content: The script content with timing indicators like [0:00]

        Returns:
            List of (timing, text) tuples or None if not in script format
        """
        import re

        # Check if content has timing indicators like [0:00]
        timing_pattern = r"\[(\d+:\d+)\](.*?)(?=\[\d+:\d+\]|$)"
        matches = re.findall(timing_pattern, content, re.DOTALL)

        if not matches:
            return None

        # Process matches into (timing, text) tuples
        script_sections = []
        for timing, text in matches:
            script_sections.append((timing, text.strip()))

        return script_sections
