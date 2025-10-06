#!/usr/bin/env python3

import boto3
import subprocess
import os
import sys

# Configurations (you can load these from env vars, config files, etc.)
ENV_PREFIX = "dev"
KEY_PATH = "../secrets/dataeisb.pem"
REGION = "us-east-1"  # Adjust if needed
INSTANCE_NAME = f"{ENV_PREFIX}-server"

def get_public_ip(instance_name, region="us-east-1"):
    ec2 = boto3.client("ec2", region_name=region)

    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Name", "Values": [instance_name]},
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )

    reservations = response.get("Reservations", [])
    if not reservations:
        print(f"❌ No running instance found with tag Name={instance_name}")
        sys.exit(1)

    instance = reservations[0]["Instances"][0]
    public_ip = instance.get("PublicIpAddress")

    if not public_ip:
        print(f"❌ Instance {instance_name} does not have a public IP.")
        sys.exit(1)

    return public_ip

def ssh_into_instance(ip, key_path):
    ssh_command = ["ssh", "-i", key_path, f"ec2-user@{ip}"]
    os.execvp("ssh", ssh_command)  # Replaces current process with SSH (like running ssh directly)

def main():
    print(f"🔍 Looking up EC2 instance with Name tag: {INSTANCE_NAME}")

    public_ip = get_public_ip(INSTANCE_NAME, REGION)
    print(f"✅ Found running instance: {public_ip}")

    print(f"🔑 Connecting to {public_ip}...")
    ssh_into_instance(public_ip, KEY_PATH)

if __name__ == "__main__":
    main()

