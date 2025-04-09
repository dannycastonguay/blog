"""
Base classes for social media platforms.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time


class SocialMediaPlatform(ABC):
    """Base class for social media platforms."""
    
    def __init__(self, name: str):
        """Initialize the platform."""
        self.name = name
    
    @abstractmethod
    def post_content(self, content: str, page_name: str, platform_folder: Optional[str] = None) -> Dict[str, Any]:
        """
        Post content to the platform.
        
        Args:
            content: The content to post
            page_name: The name of the page
            platform_folder: Path to the platform folder (for finding media)
            
        Returns:
            Dict containing the result of the posting operation
        """
        pass
    
    def find_media_files(self, platform_folder: str) -> List[str]:
        """
        Find media files in the platform folder.
        
        Args:
            platform_folder: Path to the platform folder
            
        Returns:
            List of media file paths
        """
        return []
    
    def create_success_result(self, page_name: str, content: str, post_id: str, url: str) -> Dict[str, Any]:
        """
        Create a success result dictionary.
        
        Args:
            page_name: The name of the page
            content: The content that was posted
            post_id: The ID of the post
            url: The URL of the post
            
        Returns:
            Dict containing the success result
        """
        return {
            "platform": self.name,
            "page_name": page_name,
            "id": post_id,
            "text": content,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "url": url,
            "status": "success"
        }
    
    def create_error_result(self, page_name: str, content: str, error: str) -> Dict[str, Any]:
        """
        Create an error result dictionary.
        
        Args:
            page_name: The name of the page
            content: The content that was attempted to be posted
            error: The error message
            
        Returns:
            Dict containing the error result
        """
        return {
            "platform": self.name,
            "page_name": page_name,
            "id": "",
            "text": content,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "status": "error",
            "error": error
        }
