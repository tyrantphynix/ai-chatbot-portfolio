import React, { forwardRef } from 'react';

const MessageList = forwardRef(({ messages }, ref) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 && (
        <div className="flex items-center justify-center h-full text-gray-400">
          <p>Start chatting to see messages here...</p>
        </div>
      )}
      
      {messages.map((msg, idx) => (
        <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
          <div className={`max-w-md px-4 py-2 rounded-lg ${
            msg.role === 'user' 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-200 text-gray-900'
          }`}>
            <p>{msg.content}</p>
            {msg.sources && msg.sources.length > 0 && (
              <p className="text-xs mt-2 opacity-75">
                📚 Sources: {msg.sources.join(', ')}
              </p>
            )}
          </div>
        </div>
      ))}
      <div ref={ref} />
    </div>
  );
});

MessageList.displayName = 'MessageList';
export default MessageList;
