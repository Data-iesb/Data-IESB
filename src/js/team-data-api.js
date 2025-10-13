console.log('Team Data API script loaded');

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
            console.log('API endpoint:', this.apiEndpoint);
            
            const response = await fetch(this.apiEndpoint);
            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            console.log('API response:', result);
            
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
                name: 'Prof. Sérgio da Costa Côrtes',
                role: 'Coordenador Geral',
                category: 'Coordenação',
                escavador: 'https://www.escavador.com/sobre/sergio-cortes',
                linkedin: null,
                active: true
            },
            {
                id: '2',
                email: 'simone.a.assis@iesb.edu.br',
                name: 'Profa. Simone de Araújo Góes Assis',
                role: 'Coordenadora Acadêmica',
                category: 'Coordenação',
                escavador: null,
                linkedin: null,
                active: true
            },
            {
                id: '3',
                email: 'natalia.evangelista@iesb.edu.br',
                name: 'Profa. Natália Ribeiro de Souza Evangelista',
                role: 'Coordenadora de Pesquisa',
                category: 'Coordenação',
                escavador: 'https://www.escavador.com/sobre/natalia-evangelista',
                linkedin: null,
                active: true
            },
            {
                id: '4',
                email: 'roberto.diniz@iesb.edu.br',
                name: 'Roberto Moreira Diniz',
                role: 'Especialista DevOps',
                category: 'Equipe Técnica',
                escavador: null,
                linkedin: 'https://linkedin.com/in/roberto-diniz',
                active: true
            },
            {
                id: '5',
                email: 'Ilton.ferreira@iesb.edu.com.br',
                name: 'Ilton Ferreira Mendes Neto',
                role: 'Administrador de Banco de Dados',
                category: 'Equipe Técnica',
                escavador: null,
                linkedin: null,
                active: true
            },
            {
                id: '6',
                email: 'marley.silva@iesb.edu.br',
                name: 'Marley Abe Silva',
                role: 'Desenvolvedor Full Stack',
                category: 'Equipe Técnica',
                escavador: null,
                linkedin: 'https://linkedin.com/in/marley-silva',
                active: true
            },
            {
                id: '7',
                email: 'leonardo.a.pereira@iesb.edu.br',
                name: 'Leonardo Araújo Pereira',
                role: 'Líder de Data Science',
                category: 'Equipe Técnica',
                escavador: null,
                linkedin: 'https://linkedin.com/in/leonardo-pereira',
                active: true
            },
            {
                id: '8',
                email: 'guilherme.duarte@iesb.edu.br',
                name: 'Guilherme Rocha Duarte',
                role: 'Analista de Dados e IA',
                category: 'Equipe Técnica',
                escavador: null,
                linkedin: 'https://linkedin.com/in/guilherme-duarte',
                active: true
            },
            {
                id: '9',
                email: 'leonardo.braga@iesb.edu.br',
                name: 'Leonardo Borges Silva Braga',
                role: 'Analista de Dados e IA',
                category: 'Equipe Técnica',
                escavador: null,
                linkedin: null,
                active: true
            },
            {
                id: '10',
                email: 'pedro.m.rodrigues@iesb.edu.br',
                name: 'Pedro Martins Rodrigues',
                role: 'Analista de IA',
                category: 'Equipe Técnica',
                escavador: null,
                linkedin: 'https://linkedin.com/in/pedro-rodrigues',
                active: true
            },
            {
                id: '11',
                email: 'william.w.matos@iesb.edu.br',
                name: 'William Wallace Ribeiro Matos',
                role: 'Especialista em Machine Learning',
                category: 'Equipe Técnica',
                escavador: null,
                linkedin: 'https://linkedin.com/in/william-matos',
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
        let socialLink = '';
        
        // LinkedIn for Equipe Técnica
        if (member.linkedin && member.category === 'Equipe Técnica') {
            socialLink = `
                <a href="${member.linkedin}" target="_blank" rel="noopener noreferrer" class="social-link linkedin-link" title="Conectar no LinkedIn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                    LinkedIn
                </a>
            `;
        }
        
        // Escavador for Coordination
        if (member.escavador && member.category === 'Coordenação') {
            socialLink = `
                <a href="${member.escavador}" target="_blank" rel="noopener noreferrer" class="social-link escavador-link" title="Ver perfil no Escavador">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    Escavador
                </a>
            `;
        }

        return `
            <div class="team-member">
                <strong>${member.name}</strong>
                <div class="role-badge">${member.role}</div>
                <div class="email">${member.email}</div>
                ${socialLink}
            </div>
        `;
    }

    renderTeamSection(teamData) {
        const groupedData = this.groupByCategory(teamData);
        let html = '';

        // Separate coordination from technical team
        const coordinationMembers = groupedData['Coordenação'] || [];
        const technicalMembers = [];
        
        // Group all non-coordination members as technical team
        Object.keys(groupedData).forEach(category => {
            if (category !== 'Coordenação') {
                technicalMembers.push(...groupedData[category]);
            }
        });

        // Render Coordination first
        if (coordinationMembers.length > 0) {
            html += `
                <div class="team-category">
                    <h3 class="category-title">👥 Coordenação <span class="member-count">(${coordinationMembers.length})</span></h3>
                    <div class="team-members">
            `;
            
            coordinationMembers.forEach(member => {
                html += this.renderTeamMember(member);
            });
            
            html += `
                    </div>
                </div>
            `;
        }

        // Render all technical team members together
        if (technicalMembers.length > 0) {
            const layoutClass = technicalMembers.length > 4 ? 'compact' : '';
            
            html += `
                <div class="team-category ${layoutClass}">
                    <h3 class="category-title">🔧 Equipe Técnica <span class="member-count">(${technicalMembers.length})</span></h3>
                    <div class="team-members">
            `;
            
            technicalMembers.forEach(member => {
                html += this.renderTeamMember(member);
            });
            
            html += `
                    </div>
                </div>
            `;
        }

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
            
            console.log('Fetching team data...');
            const teamData = await this.fetchTeamData();
            console.log('Team data received:', teamData);
            
            // Render the team data
            const renderedHTML = this.renderTeamSection(teamData);
            console.log('Rendered HTML length:', renderedHTML.length);
            
            teamContainer.innerHTML = renderedHTML;
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
                        <p><small>Erro: ${error.message}</small></p>
                    </div>
                `;
            }
        }
    }
}

// Initialize and load team data when the page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing team manager...');
    const teamManager = new TeamDataManager();
    console.log('Team manager created, loading team...');
    teamManager.loadAndRenderTeam();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TeamDataManager;
}
