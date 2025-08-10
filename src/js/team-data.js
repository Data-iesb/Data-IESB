class TeamDataManager {
    constructor() {
        this.tableName = 'DataIESB-Team';
        this.region = 'us-east-1';
        this.docClient = null;
        this.initializeAWS();
    }

    initializeAWS() {
        try {
            if (typeof AWS !== 'undefined') {
                AWS.config.update({
                    region: this.region,
                    credentials: new AWS.CognitoIdentityCredentials({
                        IdentityPoolId: 'us-east-1:your-identity-pool-id'
                    })
                });
                this.docClient = new AWS.DynamoDB.DocumentClient();
                console.log('AWS SDK initialized successfully');
            } else {
                console.warn('AWS SDK not available, using fallback data');
            }
        } catch (error) {
            console.warn('Failed to initialize AWS SDK:', error);
        }
    }

    async scanTable() {
        if (!this.docClient) {
            console.log('Using fallback data (AWS SDK not available)');
            return this.getFallbackData();
        }

        try {
            const params = {
                TableName: this.tableName,
                FilterExpression: 'active = :active',
                ExpressionAttributeValues: {
                    ':active': true
                }
            };

            console.log('Scanning DynamoDB table:', this.tableName);
            const result = await this.docClient.scan(params).promise();
            
            if (result.Items && result.Items.length > 0) {
                console.log(`Found ${result.Items.length} active team members in DynamoDB`);
                return result.Items;
            } else {
                console.log('No active team members found in DynamoDB, using fallback data');
                return this.getFallbackData();
            }
        } catch (error) {
            console.error('Error scanning DynamoDB table:', error);
            console.log('Falling back to static data');
            return this.getFallbackData();
        }
    }

    getFallbackData() {
        // Fallback static data with professional categories
        return [
            {
                id: '1',
                email: 'sergio.cortes@iesb.edu.br',
                name: 'Professor Sérgio da Costa Côrtes',
                role: 'Coordenação',
                category: 'Coordenação',
                active: true
            },
            {
                id: '2',
                email: 'simone.a.assis@iesb.edu.br',
                name: 'Professora Simone de Araújo Góes Assis',
                role: 'Coordenação',
                category: 'Coordenação',
                active: true
            },
            {
                id: '3',
                email: 'natalia.evangelista@iesb.edu.br',
                name: 'Professora Natália Ribeiro de Souza Evangelista',
                role: 'Coordenação',
                category: 'Coordenação',
                active: true
            },
            {
                id: '4',
                email: 'roberto.diniz@iesb.edu.br',
                name: 'Roberto Moreira Diniz',
                role: 'DevOps',
                category: 'Infraestrutura e DevOps',
                active: true
            },
            {
                id: '5',
                email: 'Ilton.ferreira@iesb.edu.com.br',
                name: 'Ilton Ferreira Mendes Neto',
                role: 'DBA',
                category: 'Database Administrator',
                active: true
            },
            {
                id: '6',
                email: 'marley.silva@iesb.edu.br',
                name: 'Marley Abe Silva',
                role: 'Developer',
                category: 'Developer',
                active: true
            },
            {
                id: '7',
                email: 'leonardo.a.pereira@iesb.edu.br',
                name: 'Leonardo Araújo Pereira',
                role: 'DataScience Team Leader',
                category: 'Líder da Equipe de DataScience',
                active: true
            },
            {
                id: '8',
                email: 'guilherme.duarte@iesb.edu.br',
                name: 'Guilherme Rocha Duarte',
                role: 'Data Scientist',
                category: 'Cientistas de Dados e Analistas de IA',
                active: true
            },
            {
                id: '9',
                email: 'leonardo.braga@iesb.edu.br',
                name: 'Leonardo Borges Silva Braga',
                role: 'Data Scientist',
                category: 'Cientistas de Dados e Analistas de IA',
                active: true
            },
            {
                id: '10',
                email: 'pedro.m.rodrigues@iesb.edu.br',
                name: 'Pedro Martins Rodrigues',
                role: 'Data Scientist',
                category: 'Cientistas de Dados e Analistas de IA',
                active: true
            },
            {
                id: '11',
                email: 'william.w.matos@iesb.edu.br',
                name: 'William Wallace Ribeiro Matos',
                role: 'Data Scientist',
                category: 'Cientistas de Dados e Analistas de IA',
                active: true
            }
        ];
    }

    groupByCategory(teamData) {
        const grouped = {};
        
        teamData.forEach(member => {
            const category = member.category || 'Outros';
            if (!grouped[category]) {
                grouped[category] = [];
            }
            grouped[category].push(member);
        });

        return grouped;
    }

    renderTeamMember(member) {
        return `
            <div class="team-member">
                <p><strong>${member.name}</strong></p>
                <p class="role-badge">${member.role}</p>
                <p class="email">${member.email}</p>
            </div>
        `;
    }

    renderTeamSection(teamData) {
        const groupedData = this.groupByCategory(teamData);
        let html = '';

        // Define the order of categories
        const categoryOrder = [
            'Coordenação',
            'Infraestrutura e DevOps',
            'Database Administrator',
            'Developer',
            'Líder da Equipe de DataScience',
            'Cientistas de Dados e Analistas de IA',
            'Outros'
        ];

        categoryOrder.forEach(category => {
            if (groupedData[category] && groupedData[category].length > 0) {
                html += `<div class="team-category">`;
                html += `<h4 class="category-title">${category}</h4>`;
                html += `<div class="team-members">`;
                
                groupedData[category].forEach(member => {
                    html += this.renderTeamMember(member);
                });
                
                html += `</div></div>`;
            }
        });

        return html;
    }

    async loadAndRenderTeam() {
        try {
            const teamData = await this.scanTable();
            
            // Render the team data
            const teamContainer = document.getElementById('dynamic-team-data');
            if (teamContainer) {
                teamContainer.innerHTML = this.renderTeamSection(teamData);
                console.log(`Rendered ${teamData.length} team members`);
            } else {
                console.warn('Team container element not found');
            }
            
        } catch (error) {
            console.error('Error loading team data:', error);
            
            // Fallback to static data
            const fallbackData = this.getFallbackData();
            const teamContainer = document.getElementById('dynamic-team-data');
            if (teamContainer) {
                teamContainer.innerHTML = this.renderTeamSection(fallbackData);
                console.log('Rendered fallback team data');
            }
        }
    }
}

// Initialize and load team data when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const teamManager = new TeamDataManager();
    teamManager.loadAndRenderTeam();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TeamDataManager;
}
