import time
import subprocess
import boto3
from datetime import datetime, timedelta
import sys
import os
import subprocess
import os
import json

from config_files import config

# Environment variables
AWS_REGION = config.AWS_REGION
ECR_REPO = config.ECR_REPO 
REPOSITORY_URI = config.REPOSITORY_URI 
CONTAINER_NAME = config.CONTAINER_NAME 
CONTAINER_PORT = config.CONTAINER_PORT 

def get_latest_image_tag():
    ecr_client = boto3.client("ecr", region_name=AWS_REGION)

    response = ecr_client.describe_images(
        repositoryName=ECR_REPO
    )

    if "imageDetails" not in response or not response["imageDetails"]:
        return None  # No images found

    latest_image = max(response["imageDetails"], key=lambda x: x["imagePushedAt"])
    
    return latest_image.get("imageTags", [None])[0]  # Return first tag or None if not tagged

def run_docker_container():
    """Runs the Docker container using the latest ECR image."""
    image_tag = "latest"

    print(f"🚀 Running Docker container with image: {REPOSITORY_URI}:{image_tag}")
    os.system(f"docker rm -f {CONTAINER_NAME}")

    cmd = [
        "docker", "run",
        "-itd",
        "--name", CONTAINER_NAME,
        "-p", CONTAINER_PORT,
        "--restart", "unless-stopped",
        f"{REPOSITORY_URI}:{image_tag}"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("✅ Docker container started successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Docker container: {e.stderr}")


if __name__ == "__main__":
    # Run the function to start the container
    run_docker_container()
