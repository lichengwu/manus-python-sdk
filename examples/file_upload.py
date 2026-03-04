#!/usr/bin/env python3
"""
File Upload Example

Demonstrates how to upload files to Manus API.
"""

import os
from pathlib import Path

from manus import Manus

# Initialize client
client = Manus(api_key=os.environ.get("MANUS_API_KEY", "your-api-key"))


def upload_file_example():
    """Example: Upload a file using create_and_upload helper."""
    
    # Method 1: Create and upload in one step (recommended)
    print("Uploading file (method 1: create_and_upload)...")
    
    file_record = client.files.create_and_upload(
        filename="example.pdf",
        file_content=Path("/path/to/your/file.pdf"),  # Can be str, Path, or bytes
        purpose="assistants",
    )
    
    print(f"File uploaded: {file_record.id}")
    print(f"Filename: {file_record.filename}")
    print(f"Status: {file_record.status}")
    
    return file_record.id


def upload_file_separate_example():
    """Example: Create file record and upload separately."""
    
    # Method 2: Create record first, then upload
    print("\nUploading file (method 2: separate steps)...")
    
    # Step 1: Create file record to get upload URL
    file_record = client.files.create(
        filename="document.pdf",
        purpose="assistants",
    )
    
    print(f"File record created: {file_record.id}")
    print(f"Upload URL: {file_record.upload_url[:50]}...")
    
    # Step 2: Upload content to presigned URL
    # Note: Upload URL expires in 3 minutes!
    file_content = b"File content here..."  # Or read from file
    
    client.files.upload(
        file_id=file_record.id,
        file_content=file_content,
        upload_url=file_record.upload_url,
    )
    
    print("File uploaded successfully!")
    
    return file_record.id


def list_files_example():
    """Example: List all uploaded files."""
    
    print("\nListing files...")
    
    files = client.files.list(limit=10)
    
    for file in files:
        print(f"  - {file.id}: {file.filename} ({file.status})")


def get_file_details_example(file_id: str):
    """Example: Get details of a specific file."""
    
    print(f"\nGetting details for file: {file_id}")
    
    file = client.files.retrieve(file_id)
    
    print(f"  ID: {file.id}")
    print(f"  Filename: {file.filename}")
    print(f"  Status: {file.status}")
    print(f"  Size: {file.size} bytes")
    print(f"  Created: {file.created_at}")


def delete_file_example(file_id: str):
    """Example: Delete a file."""
    
    print(f"\nDeleting file: {file_id}")
    
    result = client.files.delete(file_id)
    
    print(f"Deleted: {result}")


if __name__ == "__main__":
    # Run examples
    file_id = upload_file_example()
    # list_files_example()
    # get_file_details_example(file_id)
    # delete_file_example(file_id)
    
    print("\n✓ File upload example completed!")
