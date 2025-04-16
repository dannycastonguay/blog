# 🚀 Blog Social Media Automation

A robust system that automatically generates and publishes social media content for your blog posts. ✨

## Table of Contents

- [Overview](#overview)
- [Workflow](#workflow)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Creating an X Account and Getting Tokens](#creating-an-x-account-and-getting-tokens)
  - [Environment Variables](#environment-variables)
  - [Repository Settings](#repository-settings)
- [Usage](#usage)
  - [Adjusting Prompts](#adjusting-prompts)
  - [Adding Media to Posts](#adding-media-to-posts)
  - [Checking Posting Results](#checking-posting-results)
- [Adding a New Platform Integration](#adding-a-new-platform-integration)
- [Limitations](#limitations)
- [Scripts Directory Overview](#scripts-directory-overview)
- [Development Guide](#development-guide)

## 📋 Overview

This project automates the process of generating and publishing social media content for blog posts. When blog posts are added, edited, or deleted in your repository, the system automatically:

1. 🔍 Detects changed posts (new, edited, deleted)
2. ✍️ Generates tailored social media content for each platform with versioning
3. 🔄 Creates a separate pull request for each post with the generated content
4. 🚀 After merging, publishes the content to configured social media platforms

## 🔄 Workflow

The system operates in a two-step workflow:

1. **Content Generation** 📝:

   - When a page is added, edited, or renamed in the `_posts` directory (either from a push to main or a PR)
   - The first GitHub Action is triggered
   - It generates social media content using AI with proper versioning
   - Creates a separate PR for each post containing the generated content
   - PR titles and branch names include the post name, version, and date

2. **Content Publishing** 📢:
   - After the content PR is merged to main
   - The second GitHub Action is triggered
   - It publishes the content to the configured social media platforms
   - Results are recorded in the PR comments

You can check the posting results by revisiting the PR after it's merged - the results will be visible in the comments section.

## 🛠️ Setup

### Prerequisites

- GitHub repository
- OpenAI API key
- Social media accounts (X, LinkedIn, etc.)

### Creating an X Account and Getting Tokens

1. **Create an X Developer Account**:

   - Go to [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   - Sign in with your X account
   - Apply for a developer account if you don't have one

2. **Create a Project and App**:

   - In the Developer Portal, create a new Project
   - Create an App within that Project
   - Set App permissions to "Read and Write"

3. **Generate Authentication Tokens** 🔑:
   - Navigate to the "Keys and Tokens" tab
   - Generate "Consumer Keys" (API Key and Secret)
   - Generate "Access Token and Secret"
   - Save all four values securely

### Environment Variables 🔐

Create a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
X_API_KEY=your_twitter_api_key
X_API_SECRET=your_twitter_api_secret
X_ACCESS_TOKEN=your_twitter_access_token
X_ACCESS_SECRET=your_twitter_access_secret
```

### Repository Settings ⚙️

1. **Add Environment Variables to GitHub**:

   - Go to your repository on GitHub
   - Navigate to Settings > Secrets and variables > Actions
   - Add the following repository secrets:
     - `OPENAI_API_KEY`
     - `TWITTER_API_KEY`
     - `TWITTER_API_SECRET`
     - `TWITTER_ACCESS_TOKEN`
     - `TWITTER_ACCESS_SECRET`
     - `GH_PAT` (GitHub Personal Access Token)

2. **Creating a GitHub Personal Access Token (GH_PAT)**:

   - Go to your GitHub account settings
   - Navigate to Developer settings > Personal access tokens > Tokens (classic)
   - Click "Generate new token" and select "Generate new token (classic)"
   - Give your token a descriptive name
   - Set the expiration as needed (recommended: 90 days or custom expiration)
   - Select the following scopes:
     - `repo` (Full control of private repositories)
     - `workflow` (Update GitHub Action workflows)
   - Click "Generate token"
   - Copy the token immediately (you won't be able to see it again)
   - Add this token as the `GH_PAT` secret in your repository settings

3. **Configure GitHub Actions**:
   - Ensure GitHub Actions are enabled for your repository
   - The workflows will be automatically triggered when new posts are added

## 📝 Usage

### Adjusting Prompts 🤖

Prompts control how the AI generates content for each platform. They are located in the `prompts/` directory.

To adjust a prompt:

1. Edit the corresponding file (e.g., `prompts/X.txt` for Twitter)
2. Use `{content}` as a placeholder for the blog post content
3. Content instructions should be placed within brackets to clearly indicate what should be generated

Example prompt structure:

```
Summarize the following blog post into an engaging X post.
Use a direct, thoughtful style. Include a hook and end with a question.
It SHOULD NOT be more than 200 chars.

Blog Post:
{content}

X post:
```

### Content Versioning 📚

The system now supports versioning for social media content:

1. Content is stored in a versioned structure:

   ```
   social_media/your-page-name/X/v1/content.txt
   social_media/your-page-name/X/v2/content.txt
   ```

2. When a post is edited, a new version is automatically created
3. Version numbers are incremented sequentially (v1, v2, v3, etc.)
4. Version information is included in branch names, commit messages, and PR titles

### Adding Media to Posts 🖼️

To include media with your social media posts:

1. Add image or video files to the platform directory:

   ```
   social_media/your-page-name/X/image.jpg
   ```

   Or in the version-specific directory:

   ```
   social_media/your-page-name/X/v1/image.jpg
   ```

2. Supported formats:
   - Images: jpg, jpeg, png, gif
   - Videos: mp4, mov, avi

The system will automatically detect and attach these media files when posting.

> **Note about media files** 📌: When adding media files for posts, ensure they are in the same branch as the content for the publish workflow to detect them properly.

### Checking Posting Results 📊

After a PR with social media content is merged:

1. Go back to the PR page
2. Check the comments section to see posting results
3. Results include status, post URL, and any errors

## 🔌 Adding a New Platform Integration

To add support for a new social media platform:

1. **Create a Platform Class**:

   - Create a new file in `scripts/posting/platforms/` (e.g., `linkedin.py`)
   - Implement the platform class extending `SocialMediaPlatform`
   - Implement the required methods, especially `post_content()`

   Example:

   ```python
   from ..platforms import SocialMediaPlatform

   class LinkedInPlatform(SocialMediaPlatform):
       def __init__(self):
           super().__init__("LinkedIn")
           self._verify_credentials()

       def _verify_credentials(self):
           # Check for required environment variables
           pass

       def post_content(self, content, page_name, platform_folder=None):
           # Implement posting logic
           pass
   ```

2. **Register the Platform**:

   - Update `scripts/posting/poster.py` to include the new platform:

   ```python
   supported_platforms = {
       "X": TwitterPlatform,
       "LinkedIn": LinkedInPlatform,
   }
   ```

3. **Create a Prompt**:

   - Add a prompt file in the `prompts/` directory (e.g., `LinkedIn.txt`)

4. **Update Environment Variables**:
   - Add the required API keys/tokens to your `.env` file
   - Add the secrets to GitHub repository settings

## ⚠️ Limitations

Current limitations of the system:

- **X API Limits**: Be aware of X's API rate limits:
  - 17 posts per day for free tier accounts
  - Media uploads count toward daily limits
  - Check [X API documentation](https://developer.twitter.com/en/docs/twitter-api/rate-limits) for the latest limits

## 📁 Scripts Directory Overview

- `detect_new_pages.py`: Detects new, edited, and deleted posts in the repository
- `extract_social_media_content.py`: Generates versioned social media content using OpenAI
- `post_social_media.py`: Posts content to social media platforms
- `posting/`: Module containing platform implementations
  - `poster.py`: Main class for posting content with versioning support
  - `platforms/`: Directory containing platform-specific implementations
    - `twitter.py`: X platform implementation with support for versioned content

## 👨‍💻 Development Guide

To set up the project for development:

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Add environment variables**:

   - Create a `.env` file based on the variables listed above

3. **Add environment variables to GitHub**:

   - Add the required secrets to your repository settings

4. **Working with posts**:
   - Add, edit, or rename markdown files in the `_posts` directory
   - Commit and push to main or create a PR
   - The workflow will automatically:
     - Detect changes (new, edited, deleted, or renamed posts)
     - Generate versioned content for each changed post
     - Create a separate PR for each post with version information
     - Skip processing for deleted posts
   - Content will be published after the PR is merged into main

## 🔄 File Change Handling

The system handles different types of file changes:

- **New Posts**: Generates new social media content
- **Edited Posts**: Creates a new version of the social media content
- **Renamed Posts**: Treated as new posts with fresh content
- **Deleted Posts**: Skipped in the content generation process
- **Invalid Characters**: Post names with invalid Git branch characters (spaces, special characters) are automatically sanitized for branch names
- **Folder Names with Spaces**: Both the posting script and publishing workflow properly handle folder names containing spaces

## 🔧 Branch Name Handling

The system includes several features for handling branch names:

- **Sanitization**: Automatically replaces invalid Git branch characters (spaces, ~, ^, :, ?, \*, [, @{, \) with underscores
- **Versioning**: Includes version information in branch names (`{page_name}_{version}_{date}_social_media`)
- **Conflict Resolution**: Handles cases when a branch already exists by adding a timestamp
- **Suffix Preservation**: Always maintains the required `_social_media` suffix for compatibility with other workflows
