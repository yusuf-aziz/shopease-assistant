// Configuration
const API_URL = 'http://localhost:9090/chat';
const SESSION_ID = 'demo-session-' + Date.now();

// State
let messages = [];
let isTyping = false;
let selectedVoiceName = '';

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    // Set initial timestamp
    document.getElementById('initialTime').textContent = formatTime(new Date());

    // Enable/disable send button based on input
    const input = document.getElementById('messageInput');
    input.addEventListener('input', function () {
        const sendButton = document.getElementById('sendButton');
        sendButton.disabled = !this.value.trim();
    });

    // Focus on input
    input.focus();

    // Initialize Voice
    setupVoice();
});

// Format time helper
function formatTime(date) {
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    const minutesStr = minutes < 10 ? '0' + minutes : minutes;
    return hours + ':' + minutesStr + ' ' + ampm;
}

// Auto-resize textarea
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
}

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Set quick message
function setQuickMessage(message) {
    const input = document.getElementById('messageInput');
    input.value = message;
    input.focus();
    document.getElementById('sendButton').disabled = false;
    autoResize(input);
}

// Basic Markdown Parser
function parseMarkdown(text) {
    let html = escapeHtml(text);

    // Bold: **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Newlines to <br>
    html = html.replace(/\n/g, '<br>');

    // Bullet points: • or - at start of line
    html = html.replace(/(?:^|<br>)\s*[•-]\s+(.*?)(?=<br>|$)/g, '<br>• $1');

    return html;
}

// Add message to chat
function addMessage(text, sender) {
    const messagesArea = document.getElementById('messagesArea');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const timestamp = formatTime(new Date());

    // Parse Markdown for bot, simple text for user
    const content = sender === 'bot' ? parseMarkdown(text) : escapeHtml(text).replace(/\n/g, '<br>');

    messageDiv.innerHTML = `
        <div class="message-bubble">
            <div class="message-text">${content}</div>
            <div class="message-time">${timestamp}</div>
        </div>
    `;

    // Remove quick actions if they exist
    const quickActions = document.getElementById('quickActions');
    if (quickActions && sender === 'user') {
        quickActions.remove();
    }

    messagesArea.appendChild(messageDiv);
    scrollToBottom();

    messages.push({ text, sender, timestamp: new Date() });

    // Speak bot response
    if (sender === 'bot') {
        speak(text);
    }
}

// Show typing indicator
function showTypingIndicator() {
    if (isTyping) return;

    isTyping = true;
    const messagesArea = document.getElementById('messagesArea');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="typing-bubble">
            <div class="typing-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
    messagesArea.appendChild(typingDiv);
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    isTyping = false;
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Scroll to bottom
function scrollToBottom() {
    const messagesArea = document.getElementById('messagesArea');
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Send message
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();

    if (!text) return;

    // Add user message
    addMessage(text, 'user');

    // Clear input
    input.value = '';
    input.style.height = 'auto';
    document.getElementById('sendButton').disabled = true;

    // Show typing indicator
    showTypingIndicator();

    try {
        // Call API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: text,
                session_id: SESSION_ID,
                customer_id: '3001002402',
                store_wa_number: '971501234567'
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Simulate typing delay
        await new Promise(resolve => setTimeout(resolve, 800));

        // Hide typing indicator
        hideTypingIndicator();

        // Add bot response
        const botMessage = data.response || data.message || "I'm here to help! Could you please rephrase that?";
        addMessage(botMessage, 'bot');

    } catch (error) {
        console.error('Error:', error);

        // Hide typing indicator
        hideTypingIndicator();

        // Show error message
        let errorMessage = "Sorry, I'm having trouble connecting. ";

        if (error.message.includes('Failed to fetch')) {
            errorMessage += "Please make sure the server is running on http://localhost:9090";
        } else {
            errorMessage += "Please try again later.";
        }

        addMessage(errorMessage, 'bot');
    }

    // Focus back on input
    input.focus();
}

// --- Voice Interaction Logic ---

let recognition;
let isListening = false;
let synth = window.speechSynthesis;

function setupVoice() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function () {
            isListening = true;
            document.getElementById('micButton').classList.add('listening');
            document.getElementById('messageInput').placeholder = "Listening...";
        };

        recognition.onend = function () {
            isListening = false;
            document.getElementById('micButton').classList.remove('listening');
            document.getElementById('messageInput').placeholder = "Type or speak...";

            // Auto submit if text was captured
            if (document.getElementById('messageInput').value.trim()) {
                sendMessage();
            }
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('messageInput').value = transcript;
            autoResize(document.getElementById('messageInput'));
        };

        recognition.onerror = function (event) {
            console.error("Speech recognition error", event.error);
            isListening = false;
            document.getElementById('micButton').classList.remove('listening');

            let msg = "Error. Try again.";
            if (event.error === 'not-allowed') {
                msg = "Mic blocked. Allow in settings.";
                alert("Please allow Microphone access in your browser settings to use voice control.");
            } else if (event.error === 'no-speech') {
                msg = "No speech detected.";
            } else if (event.error === 'network') {
                msg = "Network error.";
            }

            document.getElementById('messageInput').placeholder = msg;
        };
    } else {
        console.log("Web Speech API not supported");
        alert("Your browser does not support Voice Recognition. Please use Chrome.");
        document.getElementById('micButton').style.display = 'none';
    }
}

function toggleVoice() {
    if (!recognition) return;

    // Always stop speaking if user clicks mic
    if (synth.speaking) {
        synth.cancel();
    }

    if (isListening) {
        recognition.stop();
    } else {
        recognition.start();
    }
}

function speak(text) {
    if (synth.speaking) {
        synth.cancel();
    }

    // Strip Markdown and Emojis for speech
    // Remove bold, bullets, newlines, and range of common emojis
    const cleanText = text
        .replace(/\*\*/g, '')          // Remove bold
        .replace(/[•\-]/g, '')         // Remove bullets
        .replace(/\n/g, '. ')          // Pause at newlines
        .replace(/[\u{1F300}-\u{1F9FF}]/gu, '') // Symbols & Pictographs
        .replace(/[\u{2600}-\u{26FF}]/gu, '')   // Misc Symbols
        .replace(/[\u{2700}-\u{27BF}]/gu, '')   // Dingbats
        .replace(/[\u{1F1E0}-\u{1F1FF}]/gu, '') // Flags
        .replace(/[\u{1F600}-\u{1F64F}]/gu, '') // Emoticons
        .replace(/[\u{1F680}-\u{1F6FF}]/gu, '') // Transport & Map
        .replace(/[\u{1F900}-\u{1F9FF}]/gu, '') // Supplemental Symbols
        .replace("👋", "");                     // Specific manual removal if needed

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'en-US';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    const voices = synth.getVoices();
    if (selectedVoiceName) {
        utterance.voice = voices.find(v => v.name === selectedVoiceName);
    } else {
        const preferredVoice = voices.find(v => v.name.includes('Google US English')) || voices[0];
        if (preferredVoice) utterance.voice = preferredVoice;
    }

    synth.speak(utterance);
}

// --- Voice Settings UI Logic ---

function openVoiceSettings() {
    populateVoiceListForModal();
    document.getElementById('voiceModal').classList.add('active');
}

function closeVoiceSettings() {
    document.getElementById('voiceModal').classList.remove('active');
}

function selectVoice(name) {
    selectedVoiceName = name;
    populateVoiceListForModal(); // Re-render to show selection
}

function previewVoice(event, name) {
    event.stopPropagation(); // Prevent selection when clicking play

    if (synth.speaking) synth.cancel();

    const utterance = new SpeechSynthesisUtterance("Hello, I am your ShopEase assistant.");
    const voices = synth.getVoices();
    utterance.voice = voices.find(v => v.name === name);
    synth.speak(utterance);
}

function populateVoiceListForModal() {
    if (typeof speechSynthesis === 'undefined') return;

    const voices = speechSynthesis.getVoices();
    const voiceList = document.getElementById('voiceList');
    voiceList.innerHTML = '';

    // Default if not set
    if (!selectedVoiceName) {
        const defaultVoice = voices.find(v => v.name.includes('Google US English')) || voices[0];
        if (defaultVoice) selectedVoiceName = defaultVoice.name;
    }

    voices.forEach((voice) => {
        // Filter for specific English accents: US and UK only
        if (['en-US', 'en-GB'].includes(voice.lang)) {
            const isSelected = voice.name === selectedVoiceName;

            const div = document.createElement('div');
            div.className = `voice-option ${isSelected ? 'selected' : ''}`;
            div.onclick = () => selectVoice(voice.name);

            div.innerHTML = `
                <div class="radio-circle"></div>
                <div class="voice-info">
                    <span class="voice-name">${voice.name.replace('Google', '').replace('English', '').trim()}</span>
                    <span class="voice-lang">${voice.lang === 'en-US' ? '🇺🇸 USA' : '🇬🇧 UK'}</span>
                </div>
                <button class="play-preview" onclick="previewVoice(event, '${voice.name}')" title="Preview Voice">
                    <svg class="icon" viewBox="0 0 24 24" fill="currentColor" stroke="none" style="width:14px;height:14px;">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                </button>
             `;

            voiceList.appendChild(div);
        }
    });
}

// Ensure voices are loaded
if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = () => {
        // If modal is open, refresh list
        if (document.getElementById('voiceModal').classList.contains('active')) {
            populateVoiceListForModal();
        }
    };
}

// Export for inline onclick handlers
window.setQuickMessage = setQuickMessage;
window.sendMessage = sendMessage;
window.handleKeyPress = handleKeyPress;
window.autoResize = autoResize;
window.toggleVoice = toggleVoice;
window.openVoiceSettings = openVoiceSettings;
window.closeVoiceSettings = closeVoiceSettings;
window.selectVoice = selectVoice;
window.previewVoice = previewVoice;