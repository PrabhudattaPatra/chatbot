// Generate a unique thread ID for new users/sessions
let threadId = crypto.randomUUID();

const toolLabels = {
    'retrieve_blog_posts': 'University Information',
    'retrieve_examination_cell_doc': 'Examination Cell',
    'retrieve_notice_board_doc': 'Official Notice Board',
    'websearch_tool': 'External Search (X)'
};

function startNewChat() {
    document.getElementById('chat-window').innerHTML = '';
    threadId = crypto.randomUUID(); // Resetting ID ensures a fresh backend state
}

async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const query = inputField.value.trim();
    if (!query) return;

    // 1. Display User Message (Left)
    appendMessage('user', query);
    inputField.value = '';

    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: query, thread_id: threadId })
        });

        const data = await response.json();
        
        // 2. Display AI Response (Right) with Tool Badge [cite: 615]
        appendMessage('ai', data.response, data.used_retrievers);
    } catch (error) {
        console.error("Error:", error);
        appendMessage('ai', "Sorry, I couldn't reach the server.");
    }
}

function appendMessage(role, text, tools = []) {
    const chatWindow = document.getElementById('chat-window');
    const wrapper = document.createElement('div');
    
    if (role === 'user') {
        wrapper.className = "user-query rounded-xl rounded-tl-none px-4 py-2 shadow-sm max-w-[80%]";
        wrapper.innerText = text;
    } else {
        wrapper.className = "ai-response-wrapper";
        
        // Add Tool Badge if tools were used
        let badgeHtml = '';
        if (tools && tools.length > 0) {
            tools.forEach(tool => {
                badgeHtml += `<span class="tool-badge">${toolLabels[tool] || tool}</span>`;
            });
        }
        
        wrapper.innerHTML = `
            ${badgeHtml}
            <div class="ai-bubble shadow-md">${text}</div>
        `;
    }

    chatWindow.appendChild(wrapper);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to bottom
}

// Allow "Enter" key to send message
document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});