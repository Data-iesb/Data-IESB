// DynamoDB Team Data Setup Script
// This script creates and populates a DynamoDB table for team members with LinkedIn profiles

const AWS = require('aws-sdk');

// Configure AWS SDK
AWS.config.update({
    region: 'us-east-1', // Change to your preferred region
    // Credentials should be configured via AWS CLI or environment variables
});

const dynamodb = new AWS.DynamoDB();
const docClient = new AWS.DynamoDB.DocumentClient();

const TABLE_NAME = 'DataIESB-Team';

// Team data with LinkedIn profiles
const teamData = [
    {
        id: '1',
        email: 'sergio.cortes@iesb.edu.br',
        name: 'Professor Sérgio da Costa Côrtes',
        role: 'Coordenação',
        category: 'Coordenação',
        linkedin: 'https://www.linkedin.com/in/sergio-cortes-iesb',
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '2',
        email: 'simone.a.assis@iesb.edu.br',
        name: 'Professora Simome de Araújo Góes Assis',
        role: 'Coordenação',
        category: 'Coordenação',
        linkedin: 'https://www.linkedin.com/in/simone-assis-iesb',
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '3',
        email: 'natalia.evangelista@iesb.edu.br',
        name: 'Professora Natália Ribeiro de Souza Evangelista',
        role: 'Coordenação',
        category: 'Coordenação',
        // No LinkedIn profile
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '4',
        email: 'roberto.diniz@iesb.edu.br',
        name: 'Roberto Moreira Diniz',
        role: 'DevOps',
        category: 'Infraestrutura e DevOps',
        linkedin: 'https://www.linkedin.com/in/roberto-diniz-devops',
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '5',
        email: 'Ilton.ferreira@iesb.edu.com.br',
        name: 'Ilton Ferreira Mendes Neto',
        role: 'DBA',
        category: 'Database Administrator',
        // No LinkedIn profile
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '6',
        email: 'marley.silva@iesb.edu.br',
        name: 'Marley Abe Silva',
        role: 'Developer',
        category: 'Developer',
        linkedin: 'https://www.linkedin.com/in/marley-silva-dev',
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '7',
        email: 'leonardo.a.pereira@iesb.edu.br',
        name: 'Leonardo Araújo Pereira',
        role: 'DataScience Team Leader',
        category: 'Líder da Equipe de DataScience',
        linkedin: 'https://www.linkedin.com/in/leonardo-pereira-datascience',
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '8',
        email: 'guilherme.duarte@iesb.edu.br',
        name: 'Guilherme Rocha Duarte',
        role: 'Data Scientist',
        category: 'Cientistas de Dados e Analistas de IA',
        linkedin: 'https://www.linkedin.com/in/guilherme-duarte-ds',
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '9',
        email: 'leonardo.braga@iesb.edu.br',
        name: 'Leonardo Borges Silva Braga',
        role: 'Data Scientist',
        category: 'Cientistas de Dados e Analistas de IA',
        // No LinkedIn profile
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '10',
        email: 'pedro.m.rodrigues@iesb.edu.br',
        name: 'Pedro Martins Rodrigues',
        role: 'Data Scientist',
        category: 'Cientistas de Dados e Analistas de IA',
        linkedin: 'https://www.linkedin.com/in/pedro-rodrigues-data',
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    },
    {
        id: '11',
        email: 'william.w.matos@iesb.edu.br',
        name: 'William Wallace Ribeiro Matos',
        role: 'Data Scientist',
        category: 'Cientistas de Dados e Analistas de IA',
        linkedin: 'https://www.linkedin.com/in/william-matos-ai',
        active: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    }
];

// Create DynamoDB table
async function createTable() {
    const params = {
        TableName: TABLE_NAME,
        KeySchema: [
            {
                AttributeName: 'id',
                KeyType: 'HASH'
            }
        ],
        AttributeDefinitions: [
            {
                AttributeName: 'id',
                AttributeType: 'S'
            },
            {
                AttributeName: 'email',
                AttributeType: 'S'
            },
            {
                AttributeName: 'category',
                AttributeType: 'S'
            }
        ],
        GlobalSecondaryIndexes: [
            {
                IndexName: 'EmailIndex',
                KeySchema: [
                    {
                        AttributeName: 'email',
                        KeyType: 'HASH'
                    }
                ],
                Projection: {
                    ProjectionType: 'ALL'
                },
                BillingMode: 'PAY_PER_REQUEST'
            },
            {
                IndexName: 'CategoryIndex',
                KeySchema: [
                    {
                        AttributeName: 'category',
                        KeyType: 'HASH'
                    }
                ],
                Projection: {
                    ProjectionType: 'ALL'
                },
                BillingMode: 'PAY_PER_REQUEST'
            }
        ],
        BillingMode: 'PAY_PER_REQUEST',
        Tags: [
            {
                Key: 'Project',
                Value: 'DataIESB'
            },
            {
                Key: 'Environment',
                Value: 'Production'
            }
        ]
    };

    try {
        const result = await dynamodb.createTable(params).promise();
        console.log('Table created successfully:', result.TableDescription.TableName);
        
        // Wait for table to be active
        await dynamodb.waitFor('tableExists', { TableName: TABLE_NAME }).promise();
        console.log('Table is now active');
        
        return true;
    } catch (error) {
        if (error.code === 'ResourceInUseException') {
            console.log('Table already exists');
            return true;
        }
        console.error('Error creating table:', error);
        return false;
    }
}

// Populate table with team data
async function populateTable() {
    console.log('Populating table with team data...');
    
    for (const member of teamData) {
        const params = {
            TableName: TABLE_NAME,
            Item: member,
            ConditionExpression: 'attribute_not_exists(id)' // Only insert if doesn't exist
        };

        try {
            await docClient.put(params).promise();
            console.log(`Added team member: ${member.name}`);
        } catch (error) {
            if (error.code === 'ConditionalCheckFailedException') {
                console.log(`Team member already exists: ${member.name}`);
            } else {
                console.error(`Error adding ${member.name}:`, error);
            }
        }
    }
}

// Update LinkedIn profile for a specific team member
async function updateLinkedInProfile(memberId, linkedinUrl) {
    const params = {
        TableName: TABLE_NAME,
        Key: { id: memberId },
        UpdateExpression: 'SET linkedin = :linkedin, updatedAt = :updatedAt',
        ExpressionAttributeValues: {
            ':linkedin': linkedinUrl,
            ':updatedAt': new Date().toISOString()
        },
        ReturnValues: 'UPDATED_NEW'
    };

    try {
        const result = await docClient.update(params).promise();
        console.log('LinkedIn profile updated:', result.Attributes);
        return result.Attributes;
    } catch (error) {
        console.error('Error updating LinkedIn profile:', error);
        throw error;
    }
}

// Get all team members
async function getAllTeamMembers() {
    const params = {
        TableName: TABLE_NAME,
        FilterExpression: 'active = :active',
        ExpressionAttributeValues: {
            ':active': true
        }
    };

    try {
        const result = await docClient.scan(params).promise();
        return result.Items;
    } catch (error) {
        console.error('Error getting team members:', error);
        throw error;
    }
}

// Get team members by category
async function getTeamMembersByCategory(category) {
    const params = {
        TableName: TABLE_NAME,
        IndexName: 'CategoryIndex',
        KeyConditionExpression: 'category = :category',
        FilterExpression: 'active = :active',
        ExpressionAttributeValues: {
            ':category': category,
            ':active': true
        }
    };

    try {
        const result = await docClient.query(params).promise();
        return result.Items;
    } catch (error) {
        console.error('Error getting team members by category:', error);
        throw error;
    }
}

// Main setup function
async function setupTeamDatabase() {
    console.log('Setting up DataIESB Team database...');
    
    const tableCreated = await createTable();
    if (tableCreated) {
        await populateTable();
        console.log('Database setup completed successfully!');
        
        // Test the setup
        console.log('\nTesting database...');
        const allMembers = await getAllTeamMembers();
        console.log(`Total active team members: ${allMembers.length}`);
        
        const membersWithLinkedIn = allMembers.filter(member => member.linkedin);
        console.log(`Members with LinkedIn profiles: ${membersWithLinkedIn.length}`);
        
        console.log('\nMembers with LinkedIn profiles:');
        membersWithLinkedIn.forEach(member => {
            console.log(`- ${member.name}: ${member.linkedin}`);
        });
    }
}

// Export functions for use in other modules
module.exports = {
    setupTeamDatabase,
    updateLinkedInProfile,
    getAllTeamMembers,
    getTeamMembersByCategory,
    TABLE_NAME
};

// Run setup if this file is executed directly
if (require.main === module) {
    setupTeamDatabase().catch(console.error);
}
