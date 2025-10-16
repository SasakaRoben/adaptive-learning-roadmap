// Chatbot Component
class Chatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.init();
    }

    init() {
        // Create chat button
        const chatButton = document.createElement('button');
        chatButton.className = 'chat-button';
        chatButton.innerHTML = '💬';
        chatButton.onclick = () => this.toggle();
        document.body.appendChild(chatButton);

        // Create chat widget
        const chatWidget = document.createElement('div');
        chatWidget.className = 'chat-widget';
        chatWidget.id = 'chatWidget';
        chatWidget.innerHTML = `
            <div class="chat-header">
                <h3>🤖 Learning Assistant</h3>
                <button class="chat-close" onclick="chatbot.close()">×</button>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    Hi! I'm your learning assistant. Ask me anything about programming, your learning path, or request a quiz!
                </div>
            </div>
            <div class="chat-input-container">
                <input type="text" class="chat-input" id="chatInput" placeholder="Type your message..." />
                <button class="chat-send" id="chatSend">➤</button>
            </div>
        `;
        document.body.appendChild(chatWidget);

        // Event listeners
        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        document.getElementById('chatSend').addEventListener('click', () => {
            this.sendMessage();
        });
    }

    toggle() {
        this.isOpen = !this.isOpen;
        const widget = document.getElementById('chatWidget');
        if (this.isOpen) {
            widget.classList.add('open');
            document.getElementById('chatInput').focus();
        } else {
            widget.classList.remove('open');
        }
    }

    close() {
        this.isOpen = false;
        document.getElementById('chatWidget').classList.remove('open');
    }

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;

        // Clear input
        input.value = '';

        // Add user message
        this.addMessage(message, 'user');

        // Show typing indicator
        this.showTyping();

        try {
            const response = await authenticatedFetch('/chatbot/ask', {
                method: 'POST',
                body: JSON.stringify({ message })
            });

            if (!response) {
                this.removeTyping();
                this.addMessage('Sorry, I could not connect. Please try again.', 'bot');
                return;
            }

            const data = await response.json();
            
            // Remove typing indicator
            this.removeTyping();

            // Add bot response
            this.addMessage(data.response, 'bot');

        } catch (error) {
            console.error('Chat error:', error);
            this.removeTyping();
            this.addMessage('Sorry, something went wrong. Please try again.', 'bot');
        }

        // Enable send button
        document.getElementById('chatSend').disabled = false;
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showTyping() {
        const messagesContainer = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot loading';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeTyping() {
        const typing = document.getElementById('typingIndicator');
        if (typing) {
            typing.remove();
        }
    }
}

// Initialize chatbot when authenticated
let chatbot;
if (typeof protectPage !== 'undefined') {
    // Only initialize on protected pages
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
            chatbot = new Chatbot();
        }, 1000);
    });
}