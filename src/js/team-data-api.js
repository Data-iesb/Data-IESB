class TeamDataManager {
    constructor() {
        // Determine API endpoint based on environment
        this.apiEndpoint = this.getApiEndpoint();
        console.log('Using API endpoint:', this.apiEndpoint);
    }

    getApiEndpoint() {
        const hostname = window.location.hostname;
        
        // Check if we're in development
        if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.includes('local')) {
            return 'http://localhost:5001/api/team';
        }
        
        // For all environments, use the deployed API Gateway endpoint
        return 'https://hewx1kjfxh.execute-api.us-east-1.amazonaws.com/prod/team';
    }

    async fetchTeamData() {
        try {
            console.log('Fetching team data from API...');
            const response = await fetch(this.apiEndpoint);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.success && result.data) {
                console.log(`✅ Loaded ${result.data.length} team members from API`);
                return result.data;
            } else {
                throw new Error(result.message || 'Failed to load team data');
            }
            
        } catch (error) {
            console.error('Error fetching team data from API:', error);
            console.log('Using fallback data');
            return this.getFallbackData();
        }
    }

    getFallbackData() {
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
                name: 'Professora Simome de Araújo Góes Assis',
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

    groupByTeacherStudent(teamData) {
        const teachers = [];
        const students = [];
        
        teamData.forEach(member => {
            // Teachers are those with "Professor" or "Professora" in name, or in Coordenação category
            if (member.name.includes('Professor') || member.name.includes('Professora') || 
                member.category === 'Coordenação') {
                teachers.push(member);
            } else {
                students.push(member);
            }
        });

        return { teachers, students };
    }

    renderTeamMember(member, isStudent = false) {
        const cardColor = isStudent ? '#D13F42' : '#1D345B';
        
        return `
            <div style="background: ${cardColor}; color: #FFFFFF; padding: 25px; border-radius: 12px; margin: 15px 0; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 1.2em; font-weight: 700; margin-bottom: 8px; color: #FFFFFF;">${member.name}</div>
                <div style="background: #FFFFFF; color: ${cardColor}; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: 600; display: inline-block; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;">${member.role}</div>
                <div style="font-size: 0.9em; color: #FFFFFF; font-weight: 400;">${member.email}</div>
            </div>
        `;
    }

    renderTeamSection(teamData) {
        const { teachers, students } = this.groupByTeacherStudent(teamData);
        
        return `
            <div style="background: #E4E4E4; padding: 40px; border-radius: 20px; margin-top: 40px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: start;">
                    <div>
                        <div style="width: 60px; height: 4px; background: #1D345B; border-radius: 2px; margin-bottom: 20px;"></div>
                        <h3 style="color: #1D345B; font-size: 1.8em; font-weight: 700; margin: 0 0 30px 0;">👨‍🏫 Coordenação</h3>
                        ${teachers.map(member => this.renderTeamMember(member, false)).join('')}
                    </div>
                    <div>
                        <div style="width: 60px; height: 4px; background: #D13F42; border-radius: 2px; margin-bottom: 20px;"></div>
                        <h3 style="color: #D13F42; font-size: 1.8em; font-weight: 700; margin: 0 0 30px 0;">👨‍💻 Equipe Técnica</h3>
                        ${students.map(member => this.renderTeamMember(member, true)).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    renderTeamSection(teamData) {
        const { teachers, students } = this.groupByTeacherStudent(teamData);
        
        return `
            <div style="display: flex; gap: 40px; align-items: flex-start;">
                <div style="flex: 1;">
                    <h3 style="color: #1D345B; border-bottom: 2px solid #1D345B; padding-bottom: 10px;">👨‍🏫 Coordenação Acadêmica</h3>
                    ${teachers.map(member => this.renderTeamMember(member, false)).join('')}
                </div>
                <div style="flex: 1;">
                    <h3 style="color: #D13F42; border-bottom: 2px solid #D13F42; padding-bottom: 10px;">👨‍💻 Equipe Técnica</h3>
                    ${students.map(member => this.renderTeamMember(member, true)).join('')}
                </div>
            </div>
        `;
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
            
            const teamData = await this.fetchTeamData();
            
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
