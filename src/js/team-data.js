class TeamDataManager {
    constructor() {
        // Configure AWS SDK for DynamoDB access
        this.tableName = 'DataIESB-Team';
        this.region = 'us-east-1'; // Change to your AWS region
        
        // Initialize AWS SDK if available
        if (typeof AWS !== 'undefined') {
            AWS.config.update({
                region: this.region
            });
            this.docClient = new AWS.DynamoDB.DocumentClient();
        } else {
            console.warn('AWS SDK not loaded, using fallback data');
            this.docClient = null;
        }
    }

    async fetchTeamDataFromDynamoDB() {
        if (!this.docClient) {
            throw new Error('AWS SDK not available');
        }

        const params = {
            TableName: this.tableName,
            FilterExpression: 'active = :active',
            ExpressionAttributeValues: {
                ':active': true
            }
        };

        try {
            const result = await this.docClient.scan(params).promise();
            return result.Items.sort((a, b) => {
                // Sort by category first, then by name
                if (a.category !== b.category) {
                    const categoryOrder = {
                        'Coordenação': 1,
                        'Infraestrutura e DevOps': 2,
                        'Database Administrator': 3,
                        'Developer': 4,
                        'Líder da Equipe de DataScience': 5,
                        'Cientistas de Dados e Analistas de IA': 6
                    };
                    return (categoryOrder[a.category] || 999) - (categoryOrder[b.category] || 999);
                }
                return a.name.localeCompare(b.name);
            });
        } catch (error) {
            console.error('Error fetching from DynamoDB:', error);
            throw error;
        }
    }

    async fetchTeamData() {
        try {
            // Try to fetch from DynamoDB first
            return await this.fetchTeamDataFromDynamoDB();
        } catch (error) {
            console.warn('DynamoDB fetch failed, using fallback data:', error);
            // Fallback to static data if DynamoDB is not available
            return this.getFallbackData();
        }
    }

    getFallbackData() {
        // Fallback static data with professional categories and LinkedIn profiles
        return [
            {
                id: '1',
                email: 'sergio.cortes@iesb.edu.br',
                name: 'Professor Sérgio da Costa Côrtes',
                role: 'Coordenação',
                category: 'Coordenação',
                linkedin: 'https://www.linkedin.com/in/sergio-cortes-iesb',
                active: true
            },
            {
                id: '2',
                email: 'simone.a.assis@iesb.edu.br',
                name: 'Professora Simome de Araújo Góes Assis',
                role: 'Coordenação',
                category: 'Coordenação',
                linkedin: 'https://www.linkedin.com/in/simone-assis-iesb',
                active: true
            },
            {
                id: '3',
                email: 'natalia.evangelista@iesb.edu.br',
                name: 'Professora Natália Ribeiro de Souza Evangelista',
                role: 'Coordenação',
                category: 'Coordenação',
                active: true
                // No LinkedIn profile
            },
            {
                id: '4',
                email: 'roberto.diniz@iesb.edu.br',
                name: 'Roberto Moreira Diniz',
                role: 'DevOps',
                category: 'Infraestrutura e DevOps',
                linkedin: 'https://www.linkedin.com/in/roberto-diniz-devops',
                active: true
            },
            {
                id: '5',
                email: 'Ilton.ferreira@iesb.edu.com.br',
                name: 'Ilton Ferreira Mendes Neto',
                role: 'DBA',
                category: 'Database Administrator',
                active: true
                // No LinkedIn profile
            },
            {
                id: '6',
                email: 'marley.silva@iesb.edu.br',
                name: 'Marley Abe Silva',
                role: 'Developer',
                category: 'Developer',
                linkedin: 'https://www.linkedin.com/in/marley-silva-dev',
                active: true
            },
            {
                id: '7',
                email: 'leonardo.a.pereira@iesb.edu.br',
                name: 'Leonardo Araújo Pereira',
                role: 'DataScience Team Leader',
                category: 'Líder da Equipe de DataScience',
                linkedin: 'https://www.linkedin.com/in/leonardo-pereira-datascience',
                active: true
            },
            {
                id: '8',
                email: 'guilherme.duarte@iesb.edu.br',
                name: 'Guilherme Rocha Duarte',
                role: 'Data Scientist',
                category: 'Cientistas de Dados e Analistas de IA',
                linkedin: 'https://www.linkedin.com/in/guilherme-duarte-ds',
                active: true
            },
            {
                id: '9',
                email: 'leonardo.braga@iesb.edu.br',
                name: 'Leonardo Borges Silva Braga',
                role: 'Data Scientist',
                category: 'Cientistas de Dados e Analistas de IA',
                active: true
                // No LinkedIn profile
            },
            {
                id: '10',
                email: 'pedro.m.rodrigues@iesb.edu.br',
                name: 'Pedro Martins Rodrigues',
                role: 'Data Scientist',
                category: 'Cientistas de Dados e Analistas de IA',
                linkedin: 'https://www.linkedin.com/in/pedro-rodrigues-data',
                active: true
            },
            {
                id: '11',
                email: 'william.w.matos@iesb.edu.br',
                name: 'William Wallace Ribeiro Matos',
                role: 'Data Scientist',
                category: 'Cientistas de Dados e Analistas de IA',
                linkedin: 'https://www.linkedin.com/in/william-matos-ai',
                active: true
            }
        ];
    }

    groupByCategory(teamMembers) {
        const grouped = {};
        
        teamMembers.forEach(member => {
            const category = member.category;
            if (!grouped[category]) {
                grouped[category] = [];
            }
            grouped[category].push(member);
        });

        return grouped;
    }

    generateLinkedInLink(member) {
        if (member.linkedin) {
            return `
                <div class="social-links">
                    <a href="${member.linkedin}" target="_blank" rel="noopener noreferrer" class="linkedin-link">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                        LinkedIn
                    </a>
                </div>
            `;
        }
        return '';
    }

    renderTeamMember(member) {
        return `
            <div class="team-member">
                <p><strong>${member.name}</strong></p>
                <p class="role-badge">${member.role}</p>
                <p class="email">${member.email}</p>
                ${this.generateLinkedInLink(member)}
            </div>
        `;
    }

    renderTeamSection(teamData) {
        const teamContainer = document.querySelector('.team-grid');
        if (!teamContainer) return;

        const grouped = this.groupByCategory(teamData);
        
        // Clear existing content
        teamContainer.innerHTML = '';

        // Create coordination column
        const coordColumn = document.createElement('div');
        coordColumn.className = 'team-column';
        
        if (grouped['Coordenação']) {
            coordColumn.innerHTML = `
                <h3>Coordenação:</h3>
                ${grouped['Coordenação'].map(member => this.renderTeamMember(member)).join('')}
            `;
        }

        // Create technical team column
        const techColumn = document.createElement('div');
        techColumn.className = 'team-column';
        
        let techContent = '';

        // Infrastructure and DevOps
        if (grouped['Infraestrutura e DevOps']) {
            techContent += `
                <h3>Infraestrutura e DevOps:</h3>
                ${grouped['Infraestrutura e DevOps'].map(member => this.renderTeamMember(member)).join('')}
            `;
        }

        // Database Administrator
        if (grouped['Database Administrator']) {
            techContent += `
                <h3>Database Administrator:</h3>
                ${grouped['Database Administrator'].map(member => this.renderTeamMember(member)).join('')}
            `;
        }

        // Developer
        if (grouped['Developer']) {
            techContent += `
                <h3>Developer:</h3>
                ${grouped['Developer'].map(member => this.renderTeamMember(member)).join('')}
            `;
        }

        // DataScience Team Leader
        if (grouped['Líder da Equipe de DataScience']) {
            techContent += `
                <h3>Líder da Equipe de DataScience:</h3>
                ${grouped['Líder da Equipe de DataScience'].map(member => this.renderTeamMember(member)).join('')}
            `;
        }

        // Data Scientists
        if (grouped['Cientistas de Dados e Analistas de IA']) {
            techContent += `
                <h3>Cientistas de Dados e Analistas de IA:</h3>
                <div class="team-member-grid">
                    ${grouped['Cientistas de Dados e Analistas de IA'].map(member => this.renderTeamMember(member)).join('')}
                </div>
            `;
        }

        techColumn.innerHTML = techContent;

        // Append columns to container
        teamContainer.appendChild(coordColumn);
        teamContainer.appendChild(techColumn);
    }

    async updateLinkedInProfile(memberId, linkedinUrl) {
        if (!this.docClient) {
            console.warn('Cannot update LinkedIn profile: AWS SDK not available');
            return false;
        }

        const params = {
            TableName: this.tableName,
            Key: { id: memberId },
            UpdateExpression: 'SET linkedin = :linkedin, updatedAt = :updatedAt',
            ExpressionAttributeValues: {
                ':linkedin': linkedinUrl,
                ':updatedAt': new Date().toISOString()
            },
            ReturnValues: 'UPDATED_NEW'
        };

        try {
            const result = await this.docClient.update(params).promise();
            console.log('LinkedIn profile updated:', result.Attributes);
            return true;
        } catch (error) {
            console.error('Error updating LinkedIn profile:', error);
            return false;
        }
    }

    async loadTeamData() {
        try {
            // Show loading state
            const teamContainer = document.querySelector('.team-grid');
            if (teamContainer) {
                teamContainer.innerHTML = '<div class="loading">Carregando dados da equipe...</div>';
            }

            const teamData = await this.fetchTeamData();
            this.renderTeamSection(teamData);
            
            // Log statistics
            const membersWithLinkedIn = teamData.filter(member => member.linkedin);
            console.log(`Loaded ${teamData.length} team members, ${membersWithLinkedIn.length} with LinkedIn profiles`);
            
        } catch (error) {
            console.error('Error loading team data:', error);
            const teamContainer = document.querySelector('.team-grid');
            if (teamContainer) {
                teamContainer.innerHTML = '<div class="error">Erro ao carregar dados da equipe. Usando dados estáticos.</div>';
                // Load fallback data
                setTimeout(() => {
                    const fallbackData = this.getFallbackData();
                    this.renderTeamSection(fallbackData);
                }, 2000);
            }
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const teamManager = new TeamDataManager();
    teamManager.loadTeamData();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TeamDataManager;
}
