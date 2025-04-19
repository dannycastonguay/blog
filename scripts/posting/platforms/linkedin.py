"""
LinkedIn platform implementation using LinkedIn API for personal profile posts
"""
import os
import glob
import requests
import mimetypes
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..platforms import SocialMediaPlatform

class LinkedInPlatform(SocialMediaPlatform):
    """LinkedIn platform implementation using LinkedIn API for personal profile posts."""
    
    def __init__(self):
        super().__init__("LinkedIn")
        self._verify_credentials()
        
    
    def _verify_credentials(self):
        required_creds = ["LINKEDIN_ACCESS_TOKEN"]
        missing = [cred for cred in required_creds if not os.getenv(cred)]
        if missing:
            raise ValueError(f"Missing credentials: {', '.join(missing)}")
    
    def _get_user_id(self) -> str:
        """Get the user's LinkedIn ID using the userinfo endpoint."""
        try:
            headers = {
                "Authorization": f"Bearer {os.getenv('LINKEDIN_ACCESS_TOKEN')}",
                "Content-Type": "application/json",
            }
            
            response = requests.get(
                "https://api.linkedin.com/v2/userinfo",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json().get("sub", "")
            else:
                error_msg = f"Failed to get user ID: {response.status_code} - {response.text}"
                self.create_error_result(
                    "LinkedIn",
                    "Unable to get user ID",
                    error_msg
                )
                raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Error getting LinkedIn user ID: {str(e)}"
            self.create_error_result(
                "LinkedIn",
                "Error getting user ID",
                error_msg
            )
            raise ValueError(error_msg)
    
    def find_media_files(self, platform_folder: str) -> List[str]:
        """
        Find media files in the platform folder.
        
        Args:
            platform_folder: Path to the platform folder
            
        Returns:
            List of media file paths
        """
        folder = os.path.dirname(platform_folder) if os.path.isfile(platform_folder) else platform_folder
        
        # Supported media extensions
        image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        video_extensions = ['mp4', 'mov', 'avi']
        
        media_files = []
        
        # Find files in current folder
        for ext in image_extensions + video_extensions:
            media_files.extend(glob.glob(os.path.join(folder, f"*.{ext}")))
        
        # Check parent folder if in version folder
        parent_folder = Path(folder).parent
        if Path(folder).name.startswith('v') and parent_folder.exists():
            for ext in image_extensions + video_extensions:
                media_files.extend(glob.glob(os.path.join(parent_folder, f"*.{ext}")))
        
        return media_files

    def post_content(
        self, 
        content: str, 
        page_name: str, 
        platform_folder: str = None
    ) -> Dict[str, Any]:
        """
        Post content to LinkedIn personal profile.
        
        Args:
            content: The content to post
            page_name: Not used (kept for compatibility)
            platform_folder: Path to the platform folder (for finding media)
            
        Returns:
            Dict containing the result of the posting operation
        """
        self.user_id = self._get_user_id()
        try:
            if not self.user_id:
                raise ValueError("LinkedIn user ID not available")
            
            # Check if there are media files
            media_files = self.find_media_files(platform_folder) if platform_folder else []
            
            if media_files:
                # Post with media
                return self._post_with_media(content, media_files)
            else:
                # Post text only
                return self._post_text_only(content)
                
        except Exception as e:
            error_msg = f"LinkedIn API Error: {str(e)}"
            return self.create_error_result(page_name, content, error_msg)
    
    def _post_text_only(self, content: str) -> Dict[str, Any]:
        """Post text content without media."""
        headers = {
            "Authorization": f"Bearer {os.getenv('LINKEDIN_ACCESS_TOKEN')}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }
        
        post_data = {
            "author": f"urn:li:person:{self.user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers,
            json=post_data
        )
        
        if response.status_code == 201:
            post_data = response.json()
            # Get the post ID from the response
            post_id = post_data.get("id", "")
            
            # Extract the activity ID from the post ID
            activity_id = post_id.split(":")[-1] if ":" in post_id else post_id
            
            # Construct the URL - use the original post ID format for the URL
            post_url = f"https://www.linkedin.com/feed/update/{post_id}"
            return self.create_success_result("personal_profile", content, post_id, post_url)
        else:
            raise ValueError(f"LinkedIn API Error: {response.status_code} - {response.text}")
    
    def _post_with_media(self, content: str, media_files: List[str]) -> Dict[str, Any]:
        """Post content with media attachments."""
        if not media_files:
            return self._post_text_only(content)
        
        media_ids = []
        for media_file in media_files:
            media_id = self._upload_media(media_file)
            if media_id:
                media_ids.append(media_id)
        
        if not media_ids:
            # Fall back to text-only post if media upload fails
            return self._post_text_only(content)
        
        # Create post with media
        headers = {
            "Authorization": f"Bearer {os.getenv('LINKEDIN_ACCESS_TOKEN')}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }
        
        # Determine media category based on the first media file
        first_media_file = media_files[0]
        mime_type, _ = mimetypes.guess_type(first_media_file)
        
        if mime_type and mime_type.startswith('video/'):
            media_category = "VIDEO"
        else:
            media_category = "IMAGE"
        
        # Create media entities
        media_entities = []
        for media_id in media_ids:
            # For videos, don't include a title/caption
            if mime_type and mime_type.startswith('video/'):
                media_entity = {
                    "status": "READY",
                    "media": media_id
                }
            else:
                media_entity = {
                    "status": "READY",
                    "media": media_id,
                    "title": {
                        "text": "Media content"
                    }
                }
            media_entities.append(media_entity)
        
        # Create post data
        post_data = {
            "author": f"urn:li:person:{self.user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": media_category,
                    "media": media_entities
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        # Send request to LinkedIn API
        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers,
            json=post_data
        )
        
        # Process response
        if response.status_code == 201:
            post_data = response.json()
            # Get the post ID from the response
            post_id = post_data.get("id", "")
            
            # Extract the activity ID from the post ID
            activity_id = post_id.split(":")[-1] if ":" in post_id else post_id
            
            # Construct the URL - use the original post ID format for the URL
            post_url = f"https://www.linkedin.com/feed/update/{post_id}"
            return self.create_success_result("personal_profile", content, post_id, post_url)
        else:
            raise ValueError(f"LinkedIn API Error: {response.status_code} - {response.text}")
    
    def _upload_media(self, media_file: str) -> Optional[str]:
        """Upload media to LinkedIn and return the media URN."""
        try:
            access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
            mime_type, _ = mimetypes.guess_type(media_file)
            
            if not mime_type:
                raise ValueError(f"Could not determine MIME type for {media_file}")
            
            # Step 1: Register upload
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            }
            
            # Determine the appropriate recipe based on media type
            is_video = mime_type and mime_type.startswith('video/')
            
            if is_video:
                recipe = "urn:li:digitalmediaRecipe:feedshare-video"
            else:
                recipe = "urn:li:digitalmediaRecipe:feedshare-image"
            
            register_data = {
                "registerUploadRequest": {
                    "recipes": [
                        recipe
                    ],
                    "owner": f"urn:li:person:{self.user_id}",
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }
            
            init_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
            
            response = requests.post(
                init_url,
                headers=headers,
                json=register_data
            )
            
            if response.status_code != 200:
                raise ValueError(f"Failed to initialize upload: {response.status_code} - {response.text}")
            
            response_json = response.json()
            
            # Extract the upload URL from the nested structure
            upload_mechanism = response_json.get("value", {}).get("uploadMechanism", {})
            upload_request = upload_mechanism.get("com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {})
            upload_url = upload_request.get("uploadUrl", "")
            
            # Get the asset ID
            asset_id = response_json.get("value", {}).get("asset", "")
            
            if not upload_url or not asset_id:
                raise ValueError("Failed to get upload URL or asset ID")
            
            # Step 2: Upload the file
            with open(media_file, "rb") as f:
                file_data = f.read()
                
                # Get additional headers if provided in the response
                additional_headers = upload_request.get("headers", {})
                
                # Set up headers with authorization and content type
                upload_headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": mime_type  # Set the correct content type based on the file
                }
                
                # Add any additional headers from the response
                upload_headers.update(additional_headers)
                
                upload_response = requests.put(
                    upload_url,
                    headers=upload_headers,
                    data=file_data
                )
            
            if upload_response.status_code not in (200, 201):
                raise ValueError(f"Failed to upload media: {upload_response.status_code} - {upload_response.text}")
            
            return asset_id
            
        except Exception as e:
            print(f"Error uploading media: {str(e)}")
            return None
