import React, { useState } from 'react';
import { BedrockAgentRuntimeClient, InvokeAgentCommand } from '@aws-sdk/client-bedrock-agent-runtime';
import { fetchAuthSession } from 'aws-amplify/auth';
import { productOpportunityConfig, enhancedProductOpportunityConfig } from './aws-config';
import './ProductOpportunityChat.css';

const ProductOpportunityChat = ({ enhanced = false }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [showLogs, setShowLogs] = useState(false);
  const [traceLogs, setTraceLogs] = useState([]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const session = await fetchAuthSession({ forceRefresh: true });
      
      if (!session.credentials) {
        throw new Error('No AWS credentials available');
      }

      const client = new BedrockAgentRuntimeClient({
        region: productOpportunityConfig.region,
        credentials: {
          accessKeyId: session.credentials.accessKeyId,
          secretAccessKey: session.credentials.secretAccessKey,
          sessionToken: session.credentials.sessionToken
        }
      });

      const currentSessionId = sessionId || `session-${Date.now()}`;
      if (!sessionId) setSessionId(currentSessionId);

      const config = enhanced ? enhancedProductOpportunityConfig : productOpportunityConfig;
      
      const command = new InvokeAgentCommand({
        agentId: config.agentId,
        agentAliasId: config.aliasId,
        sessionId: currentSessionId,
        inputText: inputMessage,
        enableTrace: enhanced
      });

      const response = await client.send(command);
      
      let assistantMessage = '';
      const logs = [];
      
      if (response.completion) {
        for await (const chunk of response.completion) {
          if (chunk.chunk?.bytes) {
            const text = new TextDecoder().decode(chunk.chunk.bytes);
            assistantMessage += text;
          }
          if (enhanced && chunk.trace) {
            logs.push({
              timestamp: new Date().toISOString(),
              type: Object.keys(chunk.trace)[0] || 'trace',
              data: chunk.trace
            });
          }
        }
      }
      
      if (enhanced) {
        setTraceLogs(prev => [...prev, ...logs]);
      }

      // Parse analysis results if present
      try {
        const analysisMatch = assistantMessage.match(/\{[\s\S]*"dcc_score"[\s\S]*\}/);
        if (analysisMatch) {
          const analysis = JSON.parse(analysisMatch[0]);
          setAnalysisResults(analysis);
        }
      } catch (e) {
        // No structured analysis found
      }

      const botMessage = { 
        role: 'assistant', 
        content: assistantMessage || 'I encountered an issue analyzing this opportunity.' 
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: `Error: ${error.message}` 
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
    setAnalysisResults(null);
    if (enhanced) {
      setTraceLogs([]);
    }
  };

  return (
    <div className="product-opportunity-chat">
      <div className="chat-header">
        <h3>{enhanced ? '🚀 Enhanced Product Analyzer' : '🎯 Product Opportunity Analyzer'}</h3>
        <div className="header-info">
          {enhanced && <span className="enhanced-badge">Real API Integration</span>}
          {enhanced && (
            <button 
              onClick={() => setShowLogs(!showLogs)} 
              className={`logs-btn ${showLogs ? 'active' : ''}`}
            >
              {showLogs ? 'Hide Logs' : 'Show Logs'}
            </button>
          )}
          <button onClick={clearChat} className="clear-btn">Clear Analysis</button>
        </div>
      </div>
      
      {showLogs && enhanced && (
        <div className="trace-logs">
          <h4>🔍 Trace Logs</h4>
          <div className="logs-container">
            {traceLogs.length === 0 ? (
              <p>No trace logs available. Logs will appear here during agent execution.</p>
            ) : (
              traceLogs.map((log, index) => (
                <div key={index} className="log-entry">
                  <div className="log-header">
                    <span className="log-timestamp">{new Date(log.timestamp).toLocaleTimeString()}</span>
                    <span className="log-type">{log.type}</span>
                  </div>
                  <div className="log-content">
                    <pre>{JSON.stringify(log.data, null, 2)}</pre>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
      
      {analysisResults && (
        <div className="analysis-dashboard">
          <h4>📊 DCC Analysis Results</h4>
          <div className="dcc-scores">
            <div className="score-card demand">
              <h5>Demand Score</h5>
              <div className="score">{analysisResults.demand_score || 0}</div>
            </div>
            <div className="score-card competition">
              <h5>Competition Score</h5>
              <div className="score">{analysisResults.competition_score || 0}</div>
            </div>
            <div className="score-card capability">
              <h5>Capability Score</h5>
              <div className="score">{analysisResults.capability_score || 0}</div>
            </div>
            <div className="score-card total">
              <h5>DCC Score</h5>
              <div className="score">{analysisResults.dcc_score || 0}</div>
            </div>
          </div>
        </div>
      )}
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>{enhanced ? '🚀 Welcome to the Enhanced Product Analyzer!' : '🎯 Welcome to the Product Opportunity Analyzer!'}</p>
            <div className="example-questions">
              <p>Try asking:</p>
              <ul>
                <li>"Analyze smart water bottle opportunity in India"</li>
                <li>"What's the potential for eco-friendly phone cases?"</li>
                <li>"Should we launch a fitness tracking app?"</li>
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
              <p>{enhanced ? 'Running enhanced analysis with real market data...' : 'Analyzing market demand, competition, and capabilities...'}</p>
            </div>
          </div>
        )}
      </div>
      
      <div className="chat-input">
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Describe your product idea or market opportunity..."
          disabled={isLoading}
          rows="2"
        />
        <button 
          onClick={sendMessage} 
          disabled={isLoading || !inputMessage.trim()}
          className="send-btn"
        >
          Analyze
        </button>
      </div>
    </div>
  );
};

export default ProductOpportunityChat;