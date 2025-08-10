class TeamDataManager {
    constructor() {
        this.tableName = 'DataIESB-TeamMembers';
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
                TableName: this.tableName
            };

            console.log('Scanning DynamoDB table:', this.tableName);
            const result = await this.docClient.scan(params).promise();
            
            if (result.Items && result.Items.length > 0) {
                console.log(`Found ${result.Items.length} team members in DynamoDB`);
                return result.Items;
            } else {
                console.log('No team members found in DynamoDB, using fallback data');
                return this.getFallbackData();
            }
        } catch (error) {
            console.error('Error scanning DynamoDB table:', error);
            console.log('Falling back to static data');
            return this.getFallbackData();
        }
    }

    getFallbackData() {
        return [
            {
                id: '1',
                email: 'sergio.cortes@iesb.edu.br',
                name: 'Prof. Sérgio da Costa Côrtes',
                role: 'Coordenador Geral',
                category: 'Coordenação',
                active: true
            },
            {
                id: '2',
                email: 'simone.a.assis@iesb.edu.br',
                name: 'Profa. Simone de Araújo Góes Assis',
                role: 'Coordenadora Acadêmica',
                category: 'Coordenação',
                active: true
            },
            {
                id: '3',
                email: 'natalia.evangelista@iesb.edu.br',
                name: 'Profa. Natália Ribeiro de Souza Evangelista',
                role: 'Coordenadora de Pesquisa',
                category: 'Coordenação',
                active: true
            },
            {
                id: '4',
                email: 'roberto.diniz@iesb.edu.br',
                name: 'Roberto Moreira Diniz',
                role: 'Especialista DevOps',
                category: 'Infraestrutura e DevOps',
                active: true
            },
            {
                id: '5',
                email: 'Ilton.ferreira@iesb.edu.com.br',
                name: 'Ilton Ferreira Mendes Neto',
                role: 'Administrador de Banco de Dados',
                category: 'Infraestrutura e DevOps',
                active: true
            },
            {
                id: '6',
                email: 'marley.silva@iesb.edu.br',
                name: 'Marley Abe Silva',
                role: 'Desenvolvedor Full Stack',
                category: 'Desenvolvimento',
                active: true
            },
            {
                id: '7',
                email: 'leonardo.a.pereira@iesb.edu.br',
                name: 'Leonardo Araújo Pereira',
                role: 'Líder de Data Science',
                category: 'Ciência de Dados',
                active: true
            },
            {
                id: '8',
                email: 'guilherme.duarte@iesb.edu.br',
                name: 'Guilherme Rocha Duarte',
                role: 'Cientista de Dados',
                category: 'Ciência de Dados',
                active: true
            },
            {
                id: '9',
                email: 'leonardo.braga@iesb.edu.br',
                name: 'Leonardo Borges Silva Braga',
                role: 'Cientista de Dados',
                category: 'Ciência de Dados',
                active: true
            },
            {
                id: '10',
                email: 'pedro.m.rodrigues@iesb.edu.br',
                name: 'Pedro Martins Rodrigues',
                role: 'Analista de IA',
                category: 'Inteligência Artificial',
                active: true
            },
            {
                id: '11',
                email: 'william.w.matos@iesb.edu.br',
                name: 'William Wallace Ribeiro Matos',
                role: 'Especialista em Machine Learning',
                category: 'Inteligência Artificial',
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
                <strong>${member.name}</strong>
                <div class="role-badge">${member.role}</div>
                <div class="email">${member.email}</div>
            </div>
        `;
    }

    renderTeamSection(teamData) {
        const groupedData = this.groupByCategory(teamData);
        let html = '';

        // Define the order of categories with better names
        const categoryOrder = [
            { key: 'Coordenação', title: '👥 Coordenação' },
            { key: 'Infraestrutura e DevOps', title: '⚙️ Infraestrutura & DevOps' },
            { key: 'Desenvolvimento', title: '💻 Desenvolvimento' },
            { key: 'Ciência de Dados', title: '📊 Ciência de Dados' },
            { key: 'Inteligência Artificial', title: '🤖 Inteligência Artificial' },
            { key: 'Outros', title: '🔧 Outros' }
        ];

        categoryOrder.forEach(({ key, title }) => {
            if (groupedData[key] && groupedData[key].length > 0) {
                html += `
                    <div class="team-category">
                        <h3 class="category-title">${title}</h3>
                        <div class="team-members">
                `;
                
                groupedData[key].forEach(member => {
                    html += this.renderTeamMember(member);
                });
                
                html += `
                        </div>
                    </div>
                `;
            }
        });

        return html;
    }

    async loadAndRenderTeam() {
        try {
            const teamContainer = document.getElementById('dynamic-team-data');
            if (!teamContainer) {
                console.warn('Team container element not found');
                return;
            }

            // Show loading state
            teamContainer.innerHTML = '<div class="loading">Carregando equipe...</div>';
            
            const teamData = await this.scanTable();
            
            // Render the team data
            teamContainer.innerHTML = this.renderTeamSection(teamData);
            teamContainer.className = 'team-grid';
            
            console.log(`✅ Rendered ${teamData.length} team members successfully`);
            
        } catch (error) {
            console.error('Error loading team data:', error);
            
            // Show error state
            const teamContainer = document.getElementById('dynamic-team-data');
            if (teamContainer) {
                teamContainer.innerHTML = `
                    <div class="error">
                        <h3>Erro ao carregar dados da equipe</h3>
                        <p>Não foi possível carregar os dados da equipe. Tente recarregar a página.</p>
                    </div>
                `;
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
