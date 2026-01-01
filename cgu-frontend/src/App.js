import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [threadId, setThreadId] = useState(uuidv4());
  const [loading, setLoading] = useState(false);

  // Map backend tool names to user-friendly labels [cite: 549, 102, 148, 191]
  const sourceLabels = {
    'retrieve_blog_posts': 'University Information',
    'retrieve_examination_cell_doc': 'Exam Cell Notice',
    'retrieve_notice_board_doc': 'Academic Notice Board',
    'websearch_tool': 'Twitter/X'
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, thread_id: threadId }),
      });

      const data = await response.json();
      
      const aiMessage = {
        role: 'ai',
        content: data.response,
        // Capture the tools used for the UI badge [cite: 541, 264, 232]
        sources: data.used_retrievers || [] 
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error calling API:", error);
    } finally {
      setLoading(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setThreadId(uuidv4()); // Resetting thread_id ensures a fresh workflow state
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto border shadow-lg bg-gray-50">
      {/* Header */}
      <div className="flex justify-between items-center p-4 border-b bg-white">
        <h1 className="font-bold text-blue-600">CGU Assistant</h1>
        <button 
          onClick={startNewChat}
          className="px-3 py-1 text-sm border rounded-lg hover:bg-gray-100"
        >
          New Chat
        </button>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
            {/* Message Bubble */}
            <div className={`p-3 rounded-2xl max-w-[85%] ${
              msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-white border text-gray-800'
            }`}>
              {msg.content}
            </div>

            {/* Tool Name Badge (Visible for AI responses if a tool was called) */}
            {msg.role === 'ai' && msg.sources?.length > 0 && (
              <div className="mt-1 flex gap-1">
                {msg.sources.map(src => (
                  <span key={src} className="text-[10px] bg-gray-200 text-gray-600 px-2 py-0.5 rounded uppercase font-bold">
                    Used: {sourceLabels[src] || src}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="text-xs text-gray-400 italic">Thinking...</div>}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t">
        <div className="flex gap-2">
          <input
            type="text"
            className="flex-1 p-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="Ask anything about CGU..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <button 
            onClick={handleSend}
            className="bg-blue-600 text-white px-4 py-2 rounded-xl"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;


// npx create-react-app cgu-frontend
// cd cgu-frontend
// npm install uuid  # To generate unique thread IDs