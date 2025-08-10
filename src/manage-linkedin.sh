#!/bin/bash

# LinkedIn Profile Management Script for DataIESB Team
# Usage: ./manage-linkedin.sh [add|remove|list] [member_id] [linkedin_url]

TABLE_NAME="DataIESB-Team"
REGION="us-east-1"

function show_usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  list                    - List all team members with their LinkedIn status"
    echo "  add [id] [url]         - Add LinkedIn profile to team member"
    echo "  remove [id]            - Remove LinkedIn profile from team member"
    echo "  show-with-linkedin     - Show only members with LinkedIn profiles"
    echo ""
    echo "Examples:"
    echo "  $0 list"
    echo "  $0 add 3 https://www.linkedin.com/in/natalia-evangelista"
    echo "  $0 remove 5"
    echo "  $0 show-with-linkedin"
}

function list_all_members() {
    echo "DataIESB Team Members and LinkedIn Status:"
    echo "=========================================="
    
    aws dynamodb scan \
        --table-name $TABLE_NAME \
        --filter-expression "active = :active" \
        --expression-attribute-values '{":active":{"BOOL":true}}' \
        --projection-expression "id, #n, email, linkedin" \
        --expression-attribute-names '{"#n": "name"}' \
        --region $REGION \
        --output json | jq -r '.Items[] | 
        "ID: " + .id.S + 
        "\nName: " + .name.S + 
        "\nEmail: " + .email.S + 
        "\nLinkedIn: " + (if .linkedin then .linkedin.S else "Not set") + 
        "\n" + ("-" * 50)'
}

function show_with_linkedin() {
    echo "Team Members with LinkedIn Profiles:"
    echo "===================================="
    
    aws dynamodb scan \
        --table-name $TABLE_NAME \
        --filter-expression "attribute_exists(linkedin) AND active = :active" \
        --expression-attribute-values '{":active":{"BOOL":true}}' \
        --projection-expression "id, #n, linkedin" \
        --expression-attribute-names '{"#n": "name"}' \
        --region $REGION \
        --output json | jq -r '.Items[] | 
        "• " + .name.S + " (" + .id.S + "): " + .linkedin.S'
}

function add_linkedin() {
    local member_id=$1
    local linkedin_url=$2
    
    if [[ -z "$member_id" || -z "$linkedin_url" ]]; then
        echo "Error: Both member ID and LinkedIn URL are required"
        echo "Usage: $0 add [member_id] [linkedin_url]"
        return 1
    fi
    
    # Validate LinkedIn URL format
    if [[ ! "$linkedin_url" =~ ^https://www\.linkedin\.com/in/ ]]; then
        echo "Warning: LinkedIn URL should start with 'https://www.linkedin.com/in/'"
        read -p "Continue anyway? (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo "Operation cancelled"
            return 1
        fi
    fi
    
    echo "Adding LinkedIn profile for member ID: $member_id"
    
    # First, check if member exists
    member_info=$(aws dynamodb get-item \
        --table-name $TABLE_NAME \
        --key "{\"id\":{\"S\":\"$member_id\"}}" \
        --projection-expression "#n" \
        --expression-attribute-names '{"#n": "name"}' \
        --region $REGION \
        --output json 2>/dev/null)
    
    if [[ -z "$member_info" || "$member_info" == "null" ]]; then
        echo "Error: Member with ID '$member_id' not found"
        return 1
    fi
    
    member_name=$(echo "$member_info" | jq -r '.Item.name.S // "Unknown"')
    echo "Found member: $member_name"
    
    # Update the LinkedIn profile
    aws dynamodb update-item \
        --table-name $TABLE_NAME \
        --key "{\"id\":{\"S\":\"$member_id\"}}" \
        --update-expression "SET linkedin = :linkedin, updatedAt = :updatedAt" \
        --expression-attribute-values "{
            \":linkedin\":{\"S\":\"$linkedin_url\"},
            \":updatedAt\":{\"S\":\"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)\"}
        }" \
        --region $REGION
    
    if [[ $? -eq 0 ]]; then
        echo "✓ LinkedIn profile added successfully for $member_name"
        echo "  URL: $linkedin_url"
    else
        echo "✗ Failed to add LinkedIn profile"
        return 1
    fi
}

function remove_linkedin() {
    local member_id=$1
    
    if [[ -z "$member_id" ]]; then
        echo "Error: Member ID is required"
        echo "Usage: $0 remove [member_id]"
        return 1
    fi
    
    echo "Removing LinkedIn profile for member ID: $member_id"
    
    # First, check if member exists and has LinkedIn
    member_info=$(aws dynamodb get-item \
        --table-name $TABLE_NAME \
        --key "{\"id\":{\"S\":\"$member_id\"}}" \
        --projection-expression "#n, linkedin" \
        --expression-attribute-names '{"#n": "name"}' \
        --region $REGION \
        --output json 2>/dev/null)
    
    if [[ -z "$member_info" || "$member_info" == "null" ]]; then
        echo "Error: Member with ID '$member_id' not found"
        return 1
    fi
    
    member_name=$(echo "$member_info" | jq -r '.Item.name.S // "Unknown"')
    current_linkedin=$(echo "$member_info" | jq -r '.Item.linkedin.S // "None"')
    
    echo "Found member: $member_name"
    echo "Current LinkedIn: $current_linkedin"
    
    if [[ "$current_linkedin" == "None" ]]; then
        echo "Member does not have a LinkedIn profile to remove"
        return 0
    fi
    
    read -p "Are you sure you want to remove the LinkedIn profile? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Operation cancelled"
        return 0
    fi
    
    # Remove the LinkedIn profile
    aws dynamodb update-item \
        --table-name $TABLE_NAME \
        --key "{\"id\":{\"S\":\"$member_id\"}}" \
        --update-expression "REMOVE linkedin SET updatedAt = :updatedAt" \
        --expression-attribute-values "{
            \":updatedAt\":{\"S\":\"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)\"}
        }" \
        --region $REGION
    
    if [[ $? -eq 0 ]]; then
        echo "✓ LinkedIn profile removed successfully for $member_name"
    else
        echo "✗ Failed to remove LinkedIn profile"
        return 1
    fi
}

# Main script logic
case "$1" in
    "list")
        list_all_members
        ;;
    "add")
        add_linkedin "$2" "$3"
        ;;
    "remove")
        remove_linkedin "$2"
        ;;
    "show-with-linkedin")
        show_with_linkedin
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
