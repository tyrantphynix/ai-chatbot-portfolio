import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const chatService = {
  sendMessage: async (message, history = []) => {
    try {
      const response = await api.post('/chat', {
        message,
        conversation_history: history
      });
      return response.data;
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  },
  
  getHistory: async () => {
    try {
      const response = await api.get('/chat/history');
      return response.data.messages;
    } catch (error) {
      console.error('History error:', error);
      throw error;
    }
  },
  
  clearHistory: async () => {
    try {
      await api.delete('/chat/history');
    } catch (error) {
      console.error('Clear error:', error);
      throw error;
    }
  }
};
