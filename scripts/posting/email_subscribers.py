"""
Email subscriber management for the blog using Supabase.
"""
import os
import requests
from typing import List, Dict, Any

class EmailSubscriberManager:
    """Manages email subscribers for the blog using Supabase."""
    
    def __init__(self):
        """Initialize the subscriber manager."""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    def _fetch_subscribers_from_supabase(self) -> List[Dict[str, Any]]:
        """
        Fetch subscribers from Supabase database.
        
        Returns:
            List of subscriber dictionaries
        """
        if not self.supabase_url or not self.supabase_key:
            print("Supabase credentials not found in environment variables")
            return []
        
        try:
            # Construct the Supabase REST API URL for the email_subscribers table
            api_url = f"{self.supabase_url}/rest/v1/email_subscribers"
            
            # Set up headers with Supabase API key
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }
            
            # Make the request to Supabase
            response = requests.get(api_url, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                subscribers = response.json()
                print(f"Successfully fetched {len(subscribers)} subscribers from Supabase")
                
                # Transform the data to match our expected format if needed
                formatted_subscribers = []
                for sub in subscribers:
                    formatted_subscribers.append({
                        "email": sub.get("email", ""),
                        "active": sub.get("active", True),
                        "id": sub.get("id", "")
                    })
                
                return formatted_subscribers
            else:
                print(f"Failed to fetch subscribers from Supabase: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Error fetching subscribers from Supabase: {str(e)}")
            return []
    
    def get_active_subscribers(self) -> List[Dict[str, Any]]:
        """Get all active subscribers."""
        subscribers = self._fetch_subscribers_from_supabase()
        return [s for s in subscribers if s.get("active", True)]
    
    def get_all_subscribers(self) -> List[Dict[str, Any]]:
        """Get all subscribers."""
        return self._fetch_subscribers_from_supabase()
