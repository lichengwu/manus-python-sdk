#!/usr/bin/env python3
"""
Projects Example

Demonstrates how to manage projects with Manus API.
"""

import os
from manus import Manus

# Initialize client
client = Manus(api_key=os.environ.get("MANUS_API_KEY", "your-api-key"))


def create_project_example():
    """Example: Create a new project."""
    
    print("Creating project...")
    
    project = client.projects.create(
        name="My AI Assistant",
        description="Project for AI assistant tasks",
        instruction="You are a helpful assistant. Always be concise and accurate.",
    )
    
    print(f"Project created: {project.id}")
    print(f"Name: {project.name}")
    print(f"Description: {project.description}")
    print(f"Instruction: {project.instruction[:50]}...")
    
    return project.id


def list_projects_example():
    """Example: List all projects."""
    
    print("\nListing projects...")
    
    projects = client.projects.list(limit=10)
    
    for project in projects:
        print(f"  - {project.id}: {project.name}")


def get_project_example(project_id: str):
    """Example: Get project details."""
    
    print(f"\nGetting project: {project_id}")
    
    project = client.projects.retrieve(project_id)
    
    print(f"  ID: {project.id}")
    print(f"  Name: {project.name}")
    print(f"  Description: {project.description}")
    print(f"  Instruction: {project.instruction}")


def update_project_example(project_id: str):
    """Example: Update a project."""
    
    print(f"\nUpdating project: {project_id}")
    
    project = client.projects.update(
        project_id,
        name="Updated Project Name",
        description="Updated description",
        instruction="You are now a creative writing assistant.",
    )
    
    print(f"Project updated: {project.id}")
    print(f"New name: {project.name}")
    print(f"New instruction: {project.instruction[:50]}...")


def delete_project_example(project_id: str):
    """Example: Delete a project."""
    
    print(f"\nDeleting project: {project_id}")
    
    result = client.projects.delete(project_id)
    
    print(f"Deleted: {result}")


def create_task_in_project_example(project_id: str):
    """Example: Create a task within a project."""
    
    print(f"\nCreating task in project: {project_id}")
    
    from openai import OpenAI
    
    client_openai = OpenAI(
        base_url="https://api.manus.im/v1",
        api_key="**",
        default_headers={
            "API_KEY": os.environ.get("MANUS_API_KEY", "your-api-key"),
        },
    )
    
    response = client_openai.responses.create(
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Analyze this document."}
                ],
            }
        ],
        extra_body={
            "task_mode": "agent",
            "agent_profile": "manus-1.6",
            "project_id": project_id,  # Assign to project
        },
    )
    
    print(f"Task created: {response.id}")
    print(f"Project instructions will be applied automatically!")
    
    return response.id


if __name__ == "__main__":
    # Run examples
    project_id = create_project_example()
    # list_projects_example()
    # get_project_example(project_id)
    # update_project_example(project_id)
    # create_task_in_project_example(project_id)
    # delete_project_example(project_id)
    
    print("\n✓ Projects example completed!")
