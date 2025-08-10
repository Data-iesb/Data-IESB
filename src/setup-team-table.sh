#!/bin/bash

# Setup script for DataIESB Team DynamoDB table
# This script creates the DynamoDB table and populates it with team data including LinkedIn profiles

TABLE_NAME="DataIESB-Team"
REGION="us-east-1"

echo "Setting up DataIESB Team table in DynamoDB..."

# Create the table
echo "Creating table: $TABLE_NAME"
aws dynamodb create-table \
    --table-name $TABLE_NAME \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=email,AttributeType=S \
        AttributeName=category,AttributeType=S \
    --key-schema \
        AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        IndexName=EmailIndex,KeySchema=[{AttributeName=email,KeyType=HASH}],Projection={ProjectionType=ALL},BillingMode=PAY_PER_REQUEST \
        IndexName=CategoryIndex,KeySchema=[{AttributeName=category,KeyType=HASH}],Projection={ProjectionType=ALL},BillingMode=PAY_PER_REQUEST \
    --billing-mode PAY_PER_REQUEST \
    --tags Key=Project,Value=DataIESB Key=Environment,Value=Production \
    --region $REGION

# Wait for table to be active
echo "Waiting for table to be active..."
aws dynamodb wait table-exists --table-name $TABLE_NAME --region $REGION

echo "Table created successfully!"

# Populate the table with team data
echo "Populating table with team data..."

# Coordination team
aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "1"},
        "email": {"S": "sergio.cortes@iesb.edu.br"},
        "name": {"S": "Professor Sérgio da Costa Côrtes"},
        "role": {"S": "Coordenação"},
        "category": {"S": "Coordenação"},
        "linkedin": {"S": "https://www.linkedin.com/in/sergio-cortes-iesb"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "2"},
        "email": {"S": "simone.a.assis@iesb.edu.br"},
        "name": {"S": "Professora Simome de Araújo Góes Assis"},
        "role": {"S": "Coordenação"},
        "category": {"S": "Coordenação"},
        "linkedin": {"S": "https://www.linkedin.com/in/simone-assis-iesb"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "3"},
        "email": {"S": "natalia.evangelista@iesb.edu.br"},
        "name": {"S": "Professora Natália Ribeiro de Souza Evangelista"},
        "role": {"S": "Coordenação"},
        "category": {"S": "Coordenação"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

# Technical team
aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "4"},
        "email": {"S": "roberto.diniz@iesb.edu.br"},
        "name": {"S": "Roberto Moreira Diniz"},
        "role": {"S": "DevOps"},
        "category": {"S": "Infraestrutura e DevOps"},
        "linkedin": {"S": "https://www.linkedin.com/in/roberto-diniz-devops"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "5"},
        "email": {"S": "Ilton.ferreira@iesb.edu.com.br"},
        "name": {"S": "Ilton Ferreira Mendes Neto"},
        "role": {"S": "DBA"},
        "category": {"S": "Database Administrator"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "6"},
        "email": {"S": "marley.silva@iesb.edu.br"},
        "name": {"S": "Marley Abe Silva"},
        "role": {"S": "Developer"},
        "category": {"S": "Developer"},
        "linkedin": {"S": "https://www.linkedin.com/in/marley-silva-dev"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "7"},
        "email": {"S": "leonardo.a.pereira@iesb.edu.br"},
        "name": {"S": "Leonardo Araújo Pereira"},
        "role": {"S": "DataScience Team Leader"},
        "category": {"S": "Líder da Equipe de DataScience"},
        "linkedin": {"S": "https://www.linkedin.com/in/leonardo-pereira-datascience"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

# Data Scientists
aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "8"},
        "email": {"S": "guilherme.duarte@iesb.edu.br"},
        "name": {"S": "Guilherme Rocha Duarte"},
        "role": {"S": "Data Scientist"},
        "category": {"S": "Cientistas de Dados e Analistas de IA"},
        "linkedin": {"S": "https://www.linkedin.com/in/guilherme-duarte-ds"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "9"},
        "email": {"S": "leonardo.braga@iesb.edu.br"},
        "name": {"S": "Leonardo Borges Silva Braga"},
        "role": {"S": "Data Scientist"},
        "category": {"S": "Cientistas de Dados e Analistas de IA"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "10"},
        "email": {"S": "pedro.m.rodrigues@iesb.edu.br"},
        "name": {"S": "Pedro Martins Rodrigues"},
        "role": {"S": "Data Scientist"},
        "category": {"S": "Cientistas de Dados e Analistas de IA"},
        "linkedin": {"S": "https://www.linkedin.com/in/pedro-rodrigues-data"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{
        "id": {"S": "11"},
        "email": {"S": "william.w.matos@iesb.edu.br"},
        "name": {"S": "William Wallace Ribeiro Matos"},
        "role": {"S": "Data Scientist"},
        "category": {"S": "Cientistas de Dados e Analistas de IA"},
        "linkedin": {"S": "https://www.linkedin.com/in/william-matos-ai"},
        "active": {"BOOL": true},
        "createdAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"},
        "updatedAt": {"S": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"}
    }' \
    --region $REGION

echo "Team data populated successfully!"

# Verify the setup
echo "Verifying table setup..."
aws dynamodb describe-table --table-name $TABLE_NAME --region $REGION --query 'Table.[TableName,TableStatus,ItemCount]' --output table

echo "Scanning for team members with LinkedIn profiles..."
aws dynamodb scan \
    --table-name $TABLE_NAME \
    --filter-expression "attribute_exists(linkedin)" \
    --projection-expression "#n, linkedin" \
    --expression-attribute-names '{"#n": "name"}' \
    --region $REGION \
    --output table

echo "Setup completed successfully!"
echo ""
echo "To update a LinkedIn profile, use:"
echo "aws dynamodb update-item --table-name $TABLE_NAME --key '{\"id\":{\"S\":\"MEMBER_ID\"}}' --update-expression 'SET linkedin = :linkedin, updatedAt = :updatedAt' --expression-attribute-values '{\":linkedin\":{\"S\":\"LINKEDIN_URL\"},\":updatedAt\":{\"S\":\"'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'\"}}' --region $REGION"
