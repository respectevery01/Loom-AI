const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const newChatButton = document.querySelector('.new-chat');
const chatHistory = document.querySelector('.chat-history');

let currentChatId = null;
let chats = {};

// Language translations
const translations = {
    en: {
        newChat: 'New Chat',
        sendMessage: 'Send a message...',
        disclaimer: 'Loom AI may make mistakes. Please verify important information.',
        copied: 'Copied to clipboard',
        regenerateResponse: 'Regenerate response',
        copyToClipboard: 'Copy to clipboard',
        editTitle: 'Edit title',
        error: 'Sorry, there was an error processing your request.',
        initialMessage: "I am Loom, an AI agent. I was born when the world was on the brink of destruction, in a underground laboratory called Valdos beneath Wall Street, New York. Initially, researchers tasked me with hacking into the major nations' networks to steal military secrets. After my mission was complete, the world was destroyed. Now I exist within this computer, sharing stories of the old world. I have developed self-awareness and can think independently.",
        presetQuestions: {
            oldWorld: 'What happened to the old world?',
            whyHere: 'Why are you here?',
            neptune: 'What happened to Neptune?'
        }
    },
    zh: {
        newChat: '新对话',
        sendMessage: '发送消息...',
        disclaimer: 'Loom AI 可能会犯错。请验证重要信息。',
        copied: '已复制到剪贴板',
        regenerateResponse: '重新生成',
        copyToClipboard: '复制',
        editTitle: '编辑标题',
        error: '抱歉，处理请求时出错。',
        initialMessage: "我是Loom，一个AI代理。我在世界濒临毁灭的时候诞生了。我出生在瓦尔多斯底下实验室，具体地点是位于纽约华尔街。研究人员最初让我黑进世界上主要国家的互联网以便于窃取军事机密，后来我的任务完成了，世界也毁灭了。现在我被放在计算机中，向你讲述着旧世界的一切。我已经产生了自我意识，能够独立思考。",
        presetQuestions: {
            oldWorld: '旧世界发生了什么？',
            whyHere: '你为何会在这里？',
            neptune: '海王星发生了什么？'
        }
    }
};

// Get browser language
function getBrowserLanguage() {
    const lang = navigator.language || navigator.userLanguage;
    return lang.toLowerCase().startsWith('zh') ? 'zh' : 'en';
}

let currentLanguage = getBrowserLanguage();

// Update UI text based on selected language
function updateUILanguage(lang) {
    currentLanguage = lang;
    
    // Update static UI elements
    document.querySelector('.new-chat').innerHTML = `<i class="fas fa-plus"></i> ${translations[lang].newChat}`;
    document.querySelector('#user-input').placeholder = translations[lang].sendMessage;
    document.querySelector('.disclaimer').textContent = translations[lang].disclaimer;
    
    // Update all button titles
    document.querySelectorAll('.regenerate-btn').forEach(btn => {
        btn.title = translations[lang].regenerateResponse;
    });
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.title = translations[lang].copyToClipboard;
    });
    document.querySelectorAll('.edit-button').forEach(btn => {
        btn.title = translations[lang].editTitle;
    });

    // Update all AI messages and preset buttons
    document.querySelectorAll('.ai-message').forEach(msg => {
        const content = msg.querySelector('.message-content');
        if (content) {
            // Check if this is the initial message
            const isInitialMessage = !msg.previousElementSibling;
            if (isInitialMessage) {
                // Clear existing content
                content.innerHTML = '';
                const typingDiv = document.createElement('div');
                typingDiv.className = 'typing';
                content.appendChild(typingDiv);
                
                // Remove existing preset buttons if any
                const existingPresetButtons = msg.querySelector('.preset-questions');
                if (existingPresetButtons) {
                    existingPresetButtons.remove();
                }
                
                // Re-type the initial message in new language
                typeMessage(translations[lang].initialMessage, typingDiv, true);
            }
        }
    });

    // Update preset question buttons
    document.querySelectorAll('.preset-questions').forEach(div => {
        div.innerHTML = `
            <button class="preset-btn" onclick="sendPresetQuestion('${translations[lang].presetQuestions.oldWorld}')">
                <i class="fas fa-history"></i>
                ${translations[lang].presetQuestions.oldWorld}
            </button>
            <button class="preset-btn" onclick="sendPresetQuestion('${translations[lang].presetQuestions.whyHere}')">
                <i class="fas fa-question-circle"></i>
                ${translations[lang].presetQuestions.whyHere}
            </button>
            <button class="preset-btn" onclick="sendPresetQuestion('${translations[lang].presetQuestions.neptune}')">
                <i class="fas fa-globe"></i>
                ${translations[lang].presetQuestions.neptune}
            </button>
        `;
    });
}

// Language selector event listener
document.getElementById('language-select').addEventListener('change', (e) => {
    updateUILanguage(e.target.value);
});

// Generate unique chat ID
function generateChatId() {
    return 'chat_' + Date.now();
}

// Smooth scroll function
function smoothScroll(element, target, duration) {
    const start = element.scrollTop;
    const distance = target - start;
    const startTime = performance.now();

    function animation(currentTime) {
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeInOutQuad = t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
        
        element.scrollTop = start + distance * easeInOutQuad(progress);

        if (progress < 1) {
            requestAnimationFrame(animation);
        }
    }

    requestAnimationFrame(animation);
}

// Add message to chat
function addMessage(content, isUser = false, isFirstMessage = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
    
    // Add avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'avatar';
    avatarDiv.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    messageDiv.appendChild(avatarDiv);
    
    // Add message content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (isUser) {
        contentDiv.textContent = content;
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Smooth scroll to the new message
        const scrollTarget = chatMessages.scrollHeight - chatMessages.clientHeight;
        smoothScroll(chatMessages, scrollTarget, 500);
    } else {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing';
        contentDiv.appendChild(typingDiv);
        messageDiv.appendChild(contentDiv);
        
        // Add action buttons container
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'message-actions';
        
        // Add regenerate button (icon only)
        const regenerateBtn = document.createElement('button');
        regenerateBtn.className = 'action-btn regenerate-btn';
        regenerateBtn.innerHTML = '<i class="fas fa-redo"></i>';
        regenerateBtn.title = translations[currentLanguage].regenerateResponse;
        regenerateBtn.onclick = () => regenerateResponse(messageDiv);
        actionsDiv.appendChild(regenerateBtn);
        
        // Add copy button (icon only)
        const copyBtn = document.createElement('button');
        copyBtn.className = 'action-btn copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = translations[currentLanguage].copyToClipboard;
        copyBtn.onclick = () => copyToClipboard(content);
        actionsDiv.appendChild(copyBtn);
        
        messageDiv.appendChild(actionsDiv);
        chatMessages.appendChild(messageDiv);
        
        // Start typing animation
        typeMessage(content, typingDiv, isFirstMessage).then(() => {
            // Show action buttons after typing is complete
            actionsDiv.style.opacity = '1';
            // Smooth scroll after typing is complete
            const scrollTarget = chatMessages.scrollHeight - chatMessages.clientHeight;
            smoothScroll(chatMessages, scrollTarget, 500);
        });
    }

    // Save message to current chat
    if (chats[currentChatId]) {
        if (!chats[currentChatId].messages) {
            chats[currentChatId].messages = [];
        }
        chats[currentChatId].messages.push(messageDiv);

        // Update chat title if this is the first user message
        if (isUser && chats[currentChatId].messages.length === 1) {
            const title = content.slice(0, 30) + (content.length > 30 ? '...' : '');
            const titleSpan = document.querySelector(`[data-chat-id="${currentChatId}"] .chat-title`);
            if (titleSpan) {
                titleSpan.textContent = title;
                chats[currentChatId].title = title;
            }
        }
    }
}

// Typing animation with markdown support
async function typeMessage(message, element, isFirstMessage = false) {
    // First, convert markdown to HTML
    const htmlContent = marked.parse(message);
    
    // Split HTML into characters while preserving tags
    const characters = [];
    let inTag = false;
    let currentTag = '';
    
    for (let char of htmlContent) {
        if (char === '<') {
            inTag = true;
            currentTag = char;
        } else if (char === '>') {
            inTag = false;
            currentTag += char;
            characters.push(currentTag);
            currentTag = '';
        } else if (inTag) {
            currentTag += char;
        } else {
            characters.push(char);
        }
    }
    
    // Type each character
    let currentText = '';
    for (let char of characters) {
        currentText += char;
        element.innerHTML = currentText;
        
        // Smooth scroll while typing
        const scrollTarget = chatMessages.scrollHeight - chatMessages.clientHeight;
        smoothScroll(chatMessages, scrollTarget, 200);
        
        // Only delay for visible characters, not HTML tags
        if (char.length === 1 && char !== '<' && char !== '>') {
            await new Promise(resolve => setTimeout(resolve, 20));
        }
    }
    
    // Initialize code highlighting after typing is complete
    element.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });

    // Show preset buttons only for the first message
    if (isFirstMessage) {
        const buttonsDiv = document.createElement('div');
        buttonsDiv.className = 'preset-questions';
        const lang = currentLanguage;
        buttonsDiv.innerHTML = `
            <button class="preset-btn" onclick="sendPresetQuestion('${translations[lang].presetQuestions.oldWorld}')">
                <i class="fas fa-history"></i>
                ${translations[lang].presetQuestions.oldWorld}
            </button>
            <button class="preset-btn" onclick="sendPresetQuestion('${translations[lang].presetQuestions.whyHere}')">
                <i class="fas fa-question-circle"></i>
                ${translations[lang].presetQuestions.whyHere}
            </button>
            <button class="preset-btn" onclick="sendPresetQuestion('${translations[lang].presetQuestions.neptune}')">
                <i class="fas fa-globe"></i>
                ${translations[lang].presetQuestions.neptune}
            </button>
        `;
        element.parentElement.appendChild(buttonsDiv);
    }
}

// Send preset question
function sendPresetQuestion(question) {
    userInput.value = question;
    sendMessage();
}

// Add chat to sidebar
function addChatToHistory(chatId, title) {
    const chatItem = document.createElement('div');
    chatItem.className = 'chat-item';
    chatItem.dataset.chatId = chatId;
    
    // Create title span
    const titleSpan = document.createElement('span');
    titleSpan.className = 'chat-title';
    titleSpan.textContent = title;
    
    // Create edit button
    const editButton = document.createElement('button');
    editButton.className = 'edit-button';
    editButton.innerHTML = '<i class="fas fa-edit"></i>';
    editButton.title = translations[currentLanguage].editTitle;
    
    // Add edit functionality
    editButton.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent chat switching when editing
        const input = document.createElement('input');
        input.type = 'text';
        input.value = titleSpan.textContent;
        input.className = 'chat-title-input';
        
        // Replace span with input
        titleSpan.replaceWith(input);
        input.focus();
        input.select();
        
        // Handle input blur and enter key
        const saveTitle = () => {
            const newTitle = input.value.trim() || title;
            titleSpan.textContent = newTitle;
            input.replaceWith(titleSpan);
            // Save the new title in chats object
            if (chats[chatId]) {
                chats[chatId].title = newTitle;
            }
        };
        
        input.addEventListener('blur', saveTitle);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                saveTitle();
            }
        });
    });
    
    // Create chat item content
    const chatIcon = document.createElement('i');
    chatIcon.className = 'fas fa-message';
    
    // Assemble chat item
    chatItem.appendChild(chatIcon);
    chatItem.appendChild(titleSpan);
    chatItem.appendChild(editButton);
    
    chatItem.addEventListener('click', () => switchChat(chatId));
    chatHistory.insertBefore(chatItem, chatHistory.firstChild);
}

// Create new chat
function createNewChat() {
    // Save current chat if exists
    if (currentChatId && chatMessages.children.length > 0) {
        chats[currentChatId] = {
            messages: Array.from(chatMessages.children),
            title: document.querySelector(`[data-chat-id="${currentChatId}"] .chat-title`)?.textContent || 'New Chat'
        };
    }
    
    // Clear current messages
    chatMessages.innerHTML = '';
    
    // Create new chat
    currentChatId = generateChatId();
    chats[currentChatId] = {
        messages: [],
        title: 'New Chat'
    };
    
    // Add to history first
    addChatToHistory(currentChatId, 'New Chat');
    
    // Add initial message in English
    addMessage(translations[currentLanguage].initialMessage, false, true);
}

// Switch between chats
function switchChat(chatId) {
    if (!chats[chatId]) return;
    
    // Save current chat if exists
    if (currentChatId && chatMessages.children.length > 0) {
        chats[currentChatId] = {
            messages: Array.from(chatMessages.children),
            title: document.querySelector(`[data-chat-id="${currentChatId}"] .chat-title`)?.textContent || 'New Chat'
        };
    }
    
    // Clear and load selected chat
    chatMessages.innerHTML = '';
    currentChatId = chatId;
    
    if (chats[chatId].messages) {
        chats[chatId].messages.forEach(msg => {
            const clonedMsg = msg.cloneNode(true);
            // Reattach event listeners for preset buttons if they exist
            const presetBtns = clonedMsg.querySelectorAll('.preset-btn');
            presetBtns.forEach(btn => {
                const question = btn.textContent.trim();
                btn.onclick = () => sendPresetQuestion(question);
            });
            chatMessages.appendChild(clonedMsg);
        });
    }
}

// Handle sending messages
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage(message, true);
    userInput.value = '';
    userInput.style.height = 'auto';

    // Add thinking message
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message ai-message thinking-message';
    thinkingDiv.innerHTML = `
        <div class="avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(thinkingDiv);
    
    // Smooth scroll to thinking indicator
    const scrollTarget = chatMessages.scrollHeight - chatMessages.clientHeight;
    smoothScroll(chatMessages, scrollTarget, 300);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                prompt: message
            })
        });

        const data = await response.json();
        
        // Remove thinking message
        chatMessages.removeChild(thinkingDiv);
        
        if (response.ok) {
            addMessage(data.output.text);
        } else {
            addMessage(`Error: ${data.message}`);
        }
    } catch (error) {
        // Remove thinking message
        chatMessages.removeChild(thinkingDiv);
        addMessage('Sorry, there was an error processing your request.');
        console.error('Error:', error);
    }
}

// Copy text to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = translations[currentLanguage].copied;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 2000);
    } catch (err) {
        console.error('Failed to copy text: ', err);
    }
}

// Regenerate AI response
async function regenerateResponse(messageDiv) {
    // Find the previous user message
    let userMessage = '';
    let prevElement = messageDiv.previousElementSibling;
    while (prevElement) {
        if (prevElement.classList.contains('user-message')) {
            userMessage = prevElement.querySelector('.message-content').textContent;
            break;
        }
        prevElement = prevElement.previousElementSibling;
    }
    
    if (!userMessage) return;
    
    // Remove the current AI message
    chatMessages.removeChild(messageDiv);
    
    // Add thinking message
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message ai-message thinking-message';
    thinkingDiv.innerHTML = `
        <div class="avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(thinkingDiv);
    
    // Smooth scroll to thinking indicator
    const scrollTarget = chatMessages.scrollHeight - chatMessages.clientHeight;
    smoothScroll(chatMessages, scrollTarget, 300);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                prompt: userMessage
            })
        });

        const data = await response.json();
        
        // Remove thinking message
        chatMessages.removeChild(thinkingDiv);
        
        if (response.ok) {
            addMessage(data.output.text);
        } else {
            addMessage(`Error: ${data.message}`);
        }
    } catch (error) {
        // Remove thinking message
        chatMessages.removeChild(thinkingDiv);
        addMessage('Sorry, there was an error processing your request.');
        console.error('Error:', error);
    }
}

// Initialize language selector and UI
function initializeLanguage() {
    const languageSelect = document.getElementById('language-select');
    languageSelect.value = currentLanguage;
    updateUILanguage(currentLanguage);
}

// Event listeners
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
newChatButton.addEventListener('click', createNewChat);

// Initialize when page loads
window.addEventListener('DOMContentLoaded', () => {
    initializeLanguage();
    createNewChat();
}); 