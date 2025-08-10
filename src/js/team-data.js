class TeamDataManager {
    constructor() {
        // Use API endpoint instead of direct DynamoDB access
        this.apiBaseUrl = 'http://localhost:3001/api';
    }

    async fetchTeamData() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/team`);
            const result = await response.json();
            
            if (result.success) {
                return result.data;
            } else {
                throw new Error(result.error || 'Failed to fetch team data');
            }
        } catch (error) {
            console.error('Error fetching team data:', error);
            // Fallback to static data if API is not available
            return this.getFallbackData();
        }
    }

    getFallbackData() {
        // Fallback static data in case API is not available
        return [
            {
                email: 'sergio.cortes@iesb.edu.br',
                name: 'Professor Sérgio da Costa Côrtes',
                role: 'Coordenação',
                category: 'Coordenação'
            },
            {
                email: 'simone.a.assis@iesb.edu.br',
                name: 'Professora Simome de Araújo Góes Assis',
                role: 'Coordenação',
                category: 'Coordenação'
            },
            {
                email: 'natalia.evangelista@iesb.edu.br',
                name: 'Professora Natália Ribeiro de Souza Evangelista',
                role: 'Coordenação',
                category: 'Coordenação'
            },
            {
                email: 'roberto.diniz@iesb.edu.br',
                name: 'Roberto Moreira Diniz',
                role: 'DevOps',
                category: 'Aluno Analista de Infraestrutura e DevOps'
            },
            {
                email: 'Ilton.ferreira@iesb.edu.com.br',
                name: 'Ilton Ferreira Mendes Neto',
                role: 'DBA',
                category: 'Aluno DBA (Database Administrator)'
            },
            {
                email: 'marley.silva@iesb.edu.br',
                name: 'Marley Abe Silva',
                role: 'Developer',
                category: 'Aluno Developer'
            },
            {
                email: 'leonardo.a.pereira@iesb.edu.br',
                name: 'Leonardo Araújo Pereira',
                role: 'DataScience Team Leader',
                category: 'Líder da Equipe de DataScience'
            },
            {
                email: 'guilherme.duarte@iesb.edu.br',
                name: 'Guilherme Rocha Duarte',
                role: 'Data Scientist',
                category: 'Alunos Cientistas de Dados e Analistas de IA'
            },
            {
                email: 'leonardo.braga@iesb.edu.br',
                name: 'Leonardo Borges Silva Braga',
                role: 'Data Scientist',
                category: 'Alunos Cientistas de Dados e Analistas de IA'
            },
            {
                email: 'pedro.m.rodrigues@iesb.edu.br',
                name: 'Pedro Martins Rodrigues',
                role: 'Data Scientist',
                category: 'Alunos Cientistas de Dados e Analistas de IA'
            },
            {
                email: 'william.w.matos@iesb.edu.br',
                name: 'William Wallace Ribeiro Matos',
                role: 'Data Scientist',
                category: 'Alunos Cientistas de Dados e Analistas de IA'
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
                ${grouped['Coordenação'].map(member => `
                    <div class="team-member">
                        <p><strong>${member.name}</strong></p>
                        <p>${member.email}</p>
                    </div>
                `).join('')}
            `;
        }

        // Create technical team column
        const techColumn = document.createElement('div');
        techColumn.className = 'team-column';
        
        let techContent = '';

        // DevOps
        if (grouped['Aluno Analista de Infraestrutura e DevOps']) {
            techContent += `
                <h3>Aluno Analista de Infraestrutura e DevOps:</h3>
                ${grouped['Aluno Analista de Infraestrutura e DevOps'].map(member => `
                    <div class="team-member">
                        <p><strong>${member.name}</strong></p>
                        <p>${member.email}</p>
                    </div>
                `).join('')}
            `;
        }

        // DBA
        if (grouped['Aluno DBA (Database Administrator)']) {
            techContent += `
                <h3>Aluno DBA (Database Administrator):</h3>
                ${grouped['Aluno DBA (Database Administrator)'].map(member => `
                    <div class="team-member">
                        <p><strong>${member.name}</strong></p>
                        <p>${member.email}</p>
                    </div>
                `).join('')}
            `;
        }

        // Developer
        if (grouped['Aluno Developer']) {
            techContent += `
                <h3>Aluno Developer:</h3>
                ${grouped['Aluno Developer'].map(member => `
                    <div class="team-member">
                        <p><strong>${member.name}</strong></p>
                        <p>${member.email}</p>
                    </div>
                `).join('')}
            `;
        }

        // DataScience Team Leader
        if (grouped['Líder da Equipe de DataScience']) {
            techContent += `
                <h3>Líder da Equipe de DataScience:</h3>
                ${grouped['Líder da Equipe de DataScience'].map(member => `
                    <div class="team-member">
                        <p><strong>${member.name}</strong></p>
                        <p>${member.email}</p>
                    </div>
                `).join('')}
            `;
        }

        // Data Scientists
        if (grouped['Alunos Cientistas de Dados e Analistas de IA']) {
            techContent += `
                <h3>Alunos Cientistas de Dados e Analistas de IA:</h3>
                <div class="team-member-grid">
                    ${grouped['Alunos Cientistas de Dados e Analistas de IA'].map(member => `
                        <div class="team-member">
                            <p><strong>${member.name}</strong></p>
                            <p>${member.email}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        techColumn.innerHTML = techContent;

        // Append columns to container
        teamContainer.appendChild(coordColumn);
        teamContainer.appendChild(techColumn);
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
