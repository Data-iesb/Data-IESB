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

os.system(f"docker start {CONTAINER_NAME}")
os.system(f"docker exec -it {CONTAINER_NAME} bash")
