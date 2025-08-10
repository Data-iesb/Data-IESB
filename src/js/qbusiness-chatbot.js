/**
 * Amazon Q Business Chatbot Widget
 * Embeddable chatbot for integration with existing web pages
 */

class QBusinessChatbot {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || 'http://localhost:5000';
        this.conversationId = null;
        this.isOpen = false;
        
        // Customization options
        this.options = {
            title: options.title || 'Assistente Q Business',
            welcomeMessage: options.welcomeMessage || 'Olá! Como posso ajudá-lo com informações sobre nossos parceiros?',
            placeholder: options.placeholder || 'Digite sua pergunta...',
            primaryColor: options.primaryColor || '#232F3E',
            accentColor: options.accentColor || '#007DBA',
            position: options.position || 'bottom-right',
            ...options
        };
        
        this.init();
    }
    
    init() {
        this.createStyles();
        this.createHTML();
        this.attachEventListeners();
    }
    
    createStyles() {
        const styles = `
            .qb-chatbot-container {
                position: fixed;
                ${this.getPositionStyles()}
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                display: none;
                flex-direction: column;
                z-index: 10000;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .qb-chatbot-header {
                background: ${this.options.primaryColor};
                color: white;
                padding: 15px;
                border-radius: 10px 10px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .qb-chatbot-header h3 {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
            }
            
            .qb-close-btn {
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .qb-chatbot-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                max-height: 350px;
                background: #fafafa;
            }
            
            .qb-message {
                margin-bottom: 12px;
                padding: 10px 14px;
                border-radius: 12px;
                max-width: 85%;
                word-wrap: break-word;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .qb-user-message {
                background: ${this.options.accentColor};
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 4px;
            }
            
            .qb-bot-message {
                background: white;
                color: #333;
                border: 1px solid #e1e1e1;
                border-bottom-left-radius: 4px;
            }
            
            .qb-chatbot-input {
                display: flex;
                padding: 15px;
                border-top: 1px solid #e1e1e1;
                background: white;
                border-radius: 0 0 10px 10px;
            }
            
            .qb-chatbot-input input {
                flex: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 20px;
                margin-right: 10px;
                font-size: 14px;
                outline: none;
            }
            
            .qb-chatbot-input input:focus {
                border-color: ${this.options.accentColor};
            }
            
            .qb-send-btn {
                background: ${this.options.accentColor};
                color: white;
                border: none;
                padding: 12px 16px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: background-color 0.2s;
            }
            
            .qb-send-btn:hover {
                background: ${this.darkenColor(this.options.accentColor, 10)};
            }
            
            .qb-send-btn:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            
            .qb-chatbot-toggle {
                position: fixed;
                ${this.getPositionStyles()}
                width: 60px;
                height: 60px;
                background: ${this.options.primaryColor};
                color: white;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                font-size: 24px;
                z-index: 10001;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            .qb-chatbot-toggle:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 16px rgba(0,0,0,0.2);
            }
            
            .qb-loading {
                opacity: 0.7;
            }
            
            .qb-typing-indicator {
                display: flex;
                align-items: center;
                padding: 10px 14px;
                background: white;
                border: 1px solid #e1e1e1;
                border-radius: 12px;
                border-bottom-left-radius: 4px;
                max-width: 85%;
                margin-bottom: 12px;
            }
            
            .qb-typing-dots {
                display: flex;
                gap: 4px;
            }
            
            .qb-typing-dot {
                width: 6px;
                height: 6px;
                background: #999;
                border-radius: 50%;
                animation: qb-typing 1.4s infinite ease-in-out;
            }
            
            .qb-typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .qb-typing-dot:nth-child(2) { animation-delay: -0.16s; }
            
            @keyframes qb-typing {
                0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
                40% { transform: scale(1); opacity: 1; }
            }
            
            @media (max-width: 480px) {
                .qb-chatbot-container {
                    width: calc(100vw - 20px);
                    height: calc(100vh - 20px);
                    bottom: 10px;
                    right: 10px;
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }
    
    getPositionStyles() {
        const positions = {
            'bottom-right': 'bottom: 20px; right: 20px;',
            'bottom-left': 'bottom: 20px; left: 20px;',
            'top-right': 'top: 20px; right: 20px;',
            'top-left': 'top: 20px; left: 20px;'
        };
        return positions[this.options.position] || positions['bottom-right'];
    }
    
    darkenColor(color, percent) {
        const num = parseInt(color.replace("#", ""), 16);
        const amt = Math.round(2.55 * percent);
        const R = (num >> 16) - amt;
        const G = (num >> 8 & 0x00FF) - amt;
        const B = (num & 0x0000FF) - amt;
        return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
            (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
            (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1);
    }
    
    createHTML() {
        const chatbotHTML = `
            <button class="qb-chatbot-toggle" id="qbChatbotToggle">💬</button>
            
            <div class="qb-chatbot-container" id="qbChatbotContainer">
                <div class="qb-chatbot-header">
                    <h3>${this.options.title}</h3>
                    <button class="qb-close-btn" id="qbCloseBtn">×</button>
                </div>
                
                <div class="qb-chatbot-messages" id="qbChatbotMessages">
                    <div class="qb-message qb-bot-message">
                        ${this.options.welcomeMessage}
                    </div>
                </div>
                
                <div class="qb-chatbot-input">
                    <input type="text" id="qbMessageInput" placeholder="${this.options.placeholder}">
                    <button class="qb-send-btn" id="qbSendBtn">Enviar</button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }
    
    attachEventListeners() {
        const toggle = document.getElementById('qbChatbotToggle');
        const closeBtn = document.getElementById('qbCloseBtn');
        const sendBtn = document.getElementById('qbSendBtn');
        const input = document.getElementById('qbMessageInput');
        
        toggle.addEventListener('click', () => this.toggleChatbot());
        closeBtn.addEventListener('click', () => this.toggleChatbot());
        sendBtn.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }
    
    toggleChatbot() {
        const container = document.getElementById('qbChatbotContainer');
        this.isOpen = !this.isOpen;
        container.style.display = this.isOpen ? 'flex' : 'none';
        
        if (this.isOpen) {
            document.getElementById('qbMessageInput').focus();
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('qbMessageInput');
        const sendBtn = document.getElementById('qbSendBtn');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Disable input while processing
        input.disabled = true;
        sendBtn.disabled = true;
        
        // Add user message
        this.addMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversationId: this.conversationId
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            if (data.success) {
                this.addMessage(data.response, 'bot');
                this.conversationId = data.conversationId;
            } else {
                this.addMessage(`Desculpe, ocorreu um erro: ${data.message || 'Erro desconhecido'}`, 'bot');
            }
            
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Erro de conexão. Verifique se o servidor está rodando e tente novamente.', 'bot');
            console.error('Chatbot Error:', error);
        } finally {
            // Re-enable input
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        }
    }
    
    addMessage(text, sender) {
        const messagesContainer = document.getElementById('qbChatbotMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `qb-message qb-${sender}-message`;
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('qbChatbotMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'qb-typing-indicator';
        typingDiv.id = 'qbTypingIndicator';
        typingDiv.innerHTML = `
            <div class="qb-typing-dots">
                <div class="qb-typing-dot"></div>
                <div class="qb-typing-dot"></div>
                <div class="qb-typing-dot"></div>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('qbTypingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
}

// Auto-initialize if configuration is provided
if (typeof window !== 'undefined') {
    window.QBusinessChatbot = QBusinessChatbot;
    
    // Auto-initialize with default settings if qbChatbotConfig is defined
    document.addEventListener('DOMContentLoaded', () => {
        if (window.qbChatbotConfig) {
            new QBusinessChatbot(window.qbChatbotConfig);
        }
    });
}
