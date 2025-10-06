#!/usr/bin/env python3

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main menu for Terraform operations."""
    
    print("🏗️  IESB Data Science Infrastructure Manager")
    print("=" * 50)
    print("1. Initialize Terraform")
    print("2. Plan Infrastructure")
    print("3. Apply Infrastructure")
    print("4. Destroy Infrastructure")
    print("5. Show Current State")
    print("6. Exit")
    print("=" * 50)
    
    while True:
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == "1":
            if run_command("terraform init", "Initializing Terraform"):
                print("📋 Terraform initialized. You can now plan or apply.")
        
        elif choice == "2":
            if run_command("terraform plan", "Planning infrastructure changes"):
                print("📋 Plan completed. Review the changes above.")
        
        elif choice == "3":
            confirm = input("⚠️  This will create/modify AWS resources. Continue? (yes/no): ")
            if confirm.lower() == "yes":
                run_command("terraform apply", "Applying infrastructure changes")
            else:
                print("❌ Apply cancelled.")
        
        elif choice == "4":
            confirm = input("⚠️  This will DESTROY all resources. Are you sure? (yes/no): ")
            if confirm.lower() == "yes":
                run_command("terraform destroy", "Destroying infrastructure")
            else:
                print("❌ Destroy cancelled.")
        
        elif choice == "5":
            run_command("terraform show", "Showing current state")
        
        elif choice == "6":
            print("👋 Goodbye!")
            sys.exit(0)
        
        else:
            print("❌ Invalid option. Please select 1-6.")

if __name__ == "__main__":
    # Check if terraform is installed
    try:
        subprocess.run(["terraform", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Terraform is not installed or not in PATH.")
        print("Please install Terraform: https://www.terraform.io/downloads.html")
        sys.exit(1)
    
    # Check if we're in the right directory
    if not os.path.exists("main.tf"):
        print("❌ main.tf not found. Please run this script from the terraform directory.")
        sys.exit(1)
    
    main()
