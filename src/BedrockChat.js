import React, { useState } from 'react';
import { BedrockAgentRuntimeClient, InvokeAgentCommand } from '@aws-sdk/client-bedrock-agent-runtime';
import { fetchAuthSession } from 'aws-amplify/auth';
import { bedrockConfig } from './aws-config';
import './BedrockChat.css';

const BedrockChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      console.log('Getting AWS credentials...');
      
      // Force refresh credentials to get latest permissions
      const session = await fetchAuthSession({ forceRefresh: true });
      
      console.log('Session:', {
        hasCredentials: !!session.credentials,
        identityId: session.identityId,
        tokens: !!session.tokens
      });
      
      if (!session.credentials) {
        throw new Error('No AWS credentials available. Make sure Identity Pool is configured.');
      }

      console.log('Invoking Bedrock agent...');
      
      // Create Bedrock client
      const client = new BedrockAgentRuntimeClient({
        region: bedrockConfig.region,
        credentials: {
          accessKeyId: session.credentials.accessKeyId,
          secretAccessKey: session.credentials.secretAccessKey,
          sessionToken: session.credentials.sessionToken
        }
      });

      // Generate session ID if not exists
      const currentSessionId = sessionId || `session-${Date.now()}`;
      if (!sessionId) setSessionId(currentSessionId);

      // Invoke agent
      const command = new InvokeAgentCommand({
        agentId: bedrockConfig.agentId,
        agentAliasId: bedrockConfig.aliasId,
        sessionId: currentSessionId,
        inputText: inputMessage
      });

      const response = await client.send(command);
      
      // Process response stream
      let assistantMessage = '';
      if (response.completion) {
        for await (const chunk of response.completion) {
          if (chunk.chunk?.bytes) {
            const text = new TextDecoder().decode(chunk.chunk.bytes);
            assistantMessage += text;
          }
        }
      }

      const botMessage = { role: 'assistant', content: assistantMessage || 'I apologize, but I encountered an issue processing your request.' };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error calling Bedrock agent:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: `Error: ${error.message}. Please check console for details.` 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
  };

  return (
    <div className="bedrock-chat">
      <div className="chat-header">
        <h3>🤖 Weather Assistant</h3>
        <button onClick={clearChat} className="clear-btn">Clear Chat</button>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>👋 Hi! I'm your weather assistant. Ask me about weather topics!</p>
            <div className="example-questions">
              <p>Try asking:</p>
              <ul>
                <li>"What's the weather like today?"</li>
                <li>"Tell me about different types of clouds"</li>
                <li>"How do hurricanes form?"</li>
              </ul>
            </div>
          </div>
        )}
        
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant">
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>
      
      <div className="chat-input">
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me about weather..."
          disabled={isLoading}
          rows="2"
        />
        <button 
          onClick={sendMessage} 
          disabled={isLoading || !inputMessage.trim()}
          className="send-btn"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default BedrockChat;