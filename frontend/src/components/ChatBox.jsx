import React, { useState, useRef, useEffect } from 'react';
import { chatService } from '../services/api';
import MessageList from './MessageList';

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => scrollToBottom(), [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await chatService.sendMessage(userMessage, messages);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.response,
        sources: response.sources 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: '❌ Error: Could not get response. Is the backend running?' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    await chatService.clearHistory();
    setMessages([]);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 shadow-lg">
        <h1 className="text-2xl font-bold">🤖 AI Chatbot</h1>
        <p className="text-sm text-blue-100">Powered by LangChain + Groq</p>
      </div>

      {/* Messages Container */}
      <MessageList messages={messages} ref={messagesEndRef} />

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4 shadow-lg">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything..."
            disabled={loading}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg disabled:bg-gray-400 transition"
          >
            {loading ? '⏳' : '📤'}
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
          >
            🗑️
          </button>
        </form>
      </div>
    </div>
  );
}
