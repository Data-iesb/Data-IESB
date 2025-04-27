import time
import json
import sys
import os
import boto3
from datetime import datetime
from datetime import timedelta


from config_files import config

ECR_REPO = config.ECR_REPO
AWS_ACCOUNT_ID = config.AWS_ACCOUNT_ID
AWS_REGION = config.AWS_REGION
REPOSITORY_URI = config.REPOSITORY_URI
DOCKER_IMAGE = config.DOCKER_IMAGE
CONTAINER_NAME = config.CONTAINER_NAME 


def build_and_push_image():
    """Build the Docker image with AWS Secrets Manager variables and STS credentials."""

    os.system(f'docker stop {CONTAINER_NAME}')
    os.system(f'docker rm -f {CONTAINER_NAME}')
    os.system(f'docker rmi -f {DOCKER_IMAGE}')

    image_tag = "latest"

    # Authenticate Docker with ECR
    os.system(f'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com')

    print("🔨 Building image with secrets ...")

    # Run the docker build command
    build_command = f"docker build --no-cache -t {DOCKER_IMAGE} -f docker/Dockerfile . "
    os.system(build_command)

    os.system(f'docker tag {DOCKER_IMAGE} "{REPOSITORY_URI}:{image_tag}"')

    os.system(f'docker push "{REPOSITORY_URI}:{image_tag}"')

    print(f"🚀 Successfully built and pushed image: {REPOSITORY_URI}:{image_tag}")

if __name__ == "__main__":
    build_and_push_image()
