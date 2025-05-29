"""
Resend platform implementation using Resend API for email sending
"""

import os
import glob
import json
import resend
import markdown
import base64
from typing import Dict, Any, List, Optional, Literal
from pathlib import Path
from ..platforms import SocialMediaPlatform
from ..email_subscribers import EmailSubscriberManager
import time

# Define content type literals
ContentType = Literal["plain", "markdown", "html"]


class ResendPlatform(SocialMediaPlatform):
    """Resend platform implementation for sending emails."""

    def __init__(self):
        super().__init__("Resend")
        self._verify_credentials()
        self.subscriber_manager = EmailSubscriberManager()

    def _verify_credentials(self):
        required_creds = ["RESEND_API_KEY"]
        missing = [cred for cred in required_creds if not os.getenv(cred)]
        if missing:
            raise ValueError(f"Missing credentials: {', '.join(missing)}")

        # Initialize Resend client
        resend.api_key = os.getenv("RESEND_API_KEY")

    def find_media_files(self, platform_folder: str) -> List[str]:
        """
        Find media files in the media folder within the version directory.

        Args:
            platform_folder: Path to the platform folder (version directory)

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

        media_files = []

        # Look for media files in the media/ subfolder within the version directory
        media_folder = os.path.join(folder, "media")
        if os.path.exists(media_folder) and os.path.isdir(media_folder):
            for ext in image_extensions:
                media_files.extend(glob.glob(os.path.join(media_folder, f"*.{ext}")))

        return media_files

    def post_content(
        self,
        content: str,
        page_name: str,
        platform_folder: str = None,
        content_type: ContentType = "markdown",
    ) -> Dict[str, Any]:
        # Extract blog post data from the original markdown file
        blog_data = self._extract_blog_post_data(page_name)
        """
        Send content via email to all subscribers using Resend.

        Args:
            content: The content to send
            page_name: The name of the page (used as email subject)
            platform_folder: Path to the platform folder (for finding media)

        Returns:
            Dict containing the result of the sending operation
        """
        try:
            # Get sender email from environment variable or use default
            from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")

            # Get active subscribers
            subscribers = self.subscriber_manager.get_active_subscribers()

            if not subscribers:
                return self.create_success_result(
                    page_name,
                    content,
                    f"",
                    "No active subscribers found.",
                )

            # Check if there are media files
            media_files = (
                self.find_media_files(platform_folder) if platform_folder else []
            )
            blog_data = self._extract_blog_post_data(page_name)
            readable_page_name = blog_data["title"]

            # Extract subject from content if it starts with "SUBJECT:"
            subject_line = None
            if content.startswith("SUBJECT:"):
                # Extract the subject line from the content
                subject_line_end = content.find("\n")
                if subject_line_end > 0:
                    subject_line = content[8:subject_line_end].strip()
                    # Remove the subject line from the content
                    content = content[subject_line_end:].strip()

            # Use extracted subject or fallback to page name
            subject = subject_line or f"Blog Post: {readable_page_name}"

            # Prepare attachments if there are media files
            attachments = []
            for media_file in media_files:
                try:
                    with open(media_file, "rb") as f:
                        file_content = f.read()
                        # Encode file content as base64 string
                        file_content_b64 = base64.b64encode(file_content).decode('utf-8')
                        filename = os.path.basename(media_file)
                        
                        # Determine MIME type based on file extension
                        file_ext = os.path.splitext(filename)[1].lower()
                        mime_type_map = {
                            '.jpg': 'image/jpeg',
                            '.jpeg': 'image/jpeg',
                            '.png': 'image/png',
                            '.gif': 'image/gif'
                        }
                        content_type = mime_type_map.get(file_ext, 'application/octet-stream')
                        
                        attachments.append({
                            "content": file_content_b64,
                            "filename": filename,
                            "type": content_type
                        })
                except Exception as e:
                    print(f"Error reading media file {media_file}: {str(e)}")

            # Get all subscriber emails
            subscriber_emails = [s.get("email") for s in subscribers]

            # Remove any None or empty emails
            subscriber_emails = [email for email in subscriber_emails if email]

            if not subscriber_emails:
                raise ValueError("No valid subscriber emails found")

            print(
                f"Sending email to {len(subscriber_emails)} subscribers in batch mode..."
            )

            # Get the base URL for the unsubscribe endpoint
            base_url = os.getenv("SUPABASE_SUBSCRIBE_FUNCTION_URL", "")
            if not base_url:
                # Fallback to constructing from SUPABASE_URL if available
                supabase_url = os.getenv("SUPABASE_URL", "")
                if supabase_url:
                    # Convert from https://project-ref.supabase.co to https://project-ref.functions.supabase.co
                    base_url = supabase_url.replace(
                        ".supabase.co", ".functions.supabase.co"
                    )
                    base_url = f"{base_url}/email_subscriptions/unsubscribe"

            # Send emails individually to each subscriber
            successful_sends = 0
            failed_sends = 0

            print(f"Sending individual emails to {len(subscribers)} subscribers...")

            for subscriber in subscribers:
                subscriber_id = subscriber.get("id", "")
                subscriber_email = subscriber.get("email", "")
                blog_data["unsubscribe_url"] = f"{base_url}?id={subscriber_id}"
                html_content = self._generate_html_email(
                    page_name, content, content_type, blog_data
                )

                if not subscriber_id or not subscriber_email:
                    print(f"Skipping subscriber with missing ID or email: {subscriber}")
                    continue

                try:
                    # Prepare email parameters for individual sending
                    params = {
                        "from": from_email,
                        "to": subscriber_email,
                        "subject": subject,
                        "html": html_content,
                        "text": content,
                    }

                    # Add attachments if any
                    if attachments:
                        params["attachments"] = attachments

                    # Send the email to the individual subscriber
                    print(f"Sending email to {subscriber_email}...")
                    response = resend.Emails.send(params)

                    # Check if send was successful
                    if response.get("id"):
                        print(f"✅ Successfully sent to {subscriber_email}")
                        successful_sends += 1
                    else:
                        print(
                            f"❌ Failed to send to {subscriber_email}: No ID returned"
                        )
                        failed_sends += 1
                    time.sleep(0.5)

                except Exception as e:
                    print(f"❌ Error sending to {subscriber_email}: {str(e)}")
                    failed_sends += 1

            # Create result based on overall success
            if successful_sends > 0:
                result_message = f"Sent to {successful_sends} subscribers"
                if failed_sends > 0:
                    result_message += f" ({failed_sends} failed)"

                return self.create_success_result(
                    page_name,
                    content,
                    f"batch-{page_name.replace(' ', '-')}",
                    f"Sent to {successful_sends} subscribers",
                )
            else:
                raise ValueError(f"Failed to send emails to any subscribers")
        except Exception as e:
            error_msg = f"Resend API Error: {str(e)}"
            return self.create_error_result(page_name, content, error_msg)

    def _generate_html_email(
        self,
        title: str,
        content: str,
        content_type: ContentType = "plain",
        blog_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate HTML email content using external template.

        Args:
            title: The title of the blog post
            content: The content of the blog post
            content_type: The type of content being provided (plain, markdown, or html)

        Returns:
            HTML formatted email content
        """
        if not blog_data:
            blog_data = {
                "title": title,
                "publish_date": "",
                "category": "",
                "page_name_without_date": title.replace(" ", "-").lower(),
            }
        # Process content based on content_type
        if content_type == "plain":
            # Convert newlines to <br> tags for plain text
            formatted_content = content.replace("\n", "<br>")
        elif content_type == "markdown":
            # Convert markdown to HTML
            try:
                # Use Python-Markdown to convert markdown to HTML
                formatted_content = markdown.markdown(
                    content, extensions=["extra", "codehilite", "tables"]
                )
            except Exception as e:
                print(f"ERROR: Failed to convert Markdown to HTML: {str(e)}")
                # Fallback to simple conversion if markdown parsing fails
                formatted_content = content.replace("\n", "<br>")
        elif content_type == "html":
            # Use HTML content as-is
            formatted_content = content
        else:
            # Default to plain text if content_type is not recognized
            print(
                f"WARNING: Unrecognized content_type '{content_type}', defaulting to plain text"
            )
            formatted_content = content.replace("\n", "<br>")

        # Load the HTML template
        template_path = os.path.join("templates", "email", "blog_post.html")

        # Get data from blog_data
        readable_title = blog_data["title"]
        publish_date = blog_data["publish_date"] or "2023-10-01"
        category = blog_data["category"]
        page_name_without_date = blog_data["page_name_without_date"]
        unsubscribe_url = blog_data["unsubscribe_url"]

        # Construct post URL with category and page name without date
        base_url = os.getenv("BLOG_BASE_URL", "https://blog.dannycastonguay.com")

        if category and category != "":
            post_url = f"{base_url}/{category.lower()}/{page_name_without_date}"
        else:
            post_url = f"{base_url}/{page_name_without_date}"

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                template = f.read()

            # Replace placeholders with actual content
            html = (
                template.replace("{{title}}", readable_title)
                .replace("{{content}}", formatted_content)
                .replace("{{publish_date}}", publish_date)
                .replace("{{post_url}}", post_url)
                .replace("{{unsubscribe_url}}", unsubscribe_url)
            )

            return html

        except Exception as e:
            print(f"ERROR: Failed to load email template: {str(e)}")
            # Fallback to a simple template if the file can't be loaded
            return f"""
            <html>
            <body>
                <h1>{title}</h1>
                <div>{formatted_content}</div>
                <p>Thank you for subscribing to our blog updates!</p>
            </body>
            </html>
            """

    def get_subscribers(self) -> List[Dict[str, Any]]:
        """Get all active subscribers."""
        return self.subscriber_manager.get_active_subscribers()

    def _extract_blog_post_data(self, page_name: str) -> Dict[str, Any]:
        """
        Extract data from the original blog post file.

        Args:
            page_name: The name of the page (filename without extension)

        Returns:
            Dict containing blog post data (title, category, publish_date, etc.)
        """
        import yaml
        import os
        from pathlib import Path

        # Initialize default data
        data = {
            "title": page_name.replace("-", " ").title(),
            "category": "",
            "publish_date": "",
            "page_name_without_date": page_name,
        }

        # Extract date from page_name if it has a date prefix (YYYY-MM-DD-)
        if (
            len(page_name) > 11
            and page_name[4] == "-"
            and page_name[7] == "-"
            and page_name[10] == "-"
        ):
            data["publish_date"] = page_name[:10]  # Extract YYYY-MM-DD
            data["page_name_without_date"] = page_name[11:]  # Remove date prefix
            data["title"] = data["page_name_without_date"].replace("-", " ").title()

        # Try to find the original blog post file
        posts_dir = "_posts"
        possible_filenames = [
            f"{posts_dir}/{page_name}.md",  # Try exact match first
            f"{posts_dir}/{data['publish_date']}-{data['page_name_without_date']}.md",  # Try with date prefix
        ]

        blog_file_path = None
        for filename in possible_filenames:
            if os.path.exists(filename):
                blog_file_path = filename
                break

        if not blog_file_path:
            print(f"WARNING: Could not find original blog post file for {page_name}")
            return data

        # Read the blog post file
        try:
            with open(blog_file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract front matter
            parts = content.split("---", 2)
            if len(parts) >= 3:
                front_matter = yaml.safe_load(parts[1])

                # Extract data from front matter
                if front_matter:
                    # Get title from front matter
                    if "title" in front_matter:
                        data["title"] = front_matter["title"]

                    # Get category from front matter - only use 'category' field
                    if "category" in front_matter:
                        data["category"] = front_matter["category"]

            return data

        except Exception as e:
            print(f"ERROR: Failed to extract blog post data: {str(e)}")
            return data
