#!/usr/bin/env python
"""
Script to manage email subscribers for the blog.
"""
import os
import sys
import argparse
from typing import List, Dict, Any

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.posting.email_subscribers import EmailSubscriberManager

def list_subscribers(manager: EmailSubscriberManager, args: argparse.Namespace) -> None:
    """List all subscribers."""
    if args.all:
        subscribers = manager.get_all_subscribers()
    else:
        subscribers = manager.get_active_subscribers()
    
    if not subscribers:
        print("No subscribers found.")
        return
    
    print(f"Found {len(subscribers)} subscribers:")
    print("-" * 50)
    for i, subscriber in enumerate(subscribers, 1):
        status = "Active" if subscriber.get("active", True) else "Inactive"
        email = subscriber.get("email", "")
        print(f"{i}. {email} ({status})")
    print("-" * 50)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Manage email subscribers for the blog")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List subscribers
    list_parser = subparsers.add_parser("list", help="List subscribers")
    list_parser.add_argument("--all", action="store_true", help="Include inactive subscribers")
    
    args = parser.parse_args()
    
    # Initialize subscriber manager
    manager = EmailSubscriberManager()
    
    # Execute command
    if args.command == "list":
        list_subscribers(manager, args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
