import React, { useState } from 'react';
import BedrockChat from './BedrockChat';
import ProductOpportunityChat from './ProductOpportunityChat';

function ProductDashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('opportunity');

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome back, {user?.username || user?.signInDetails?.loginId}! 👋</h1>
        <button className="logout-btn" onClick={onLogout}>Sign Out</button>
      </div>
      
      <div className="tab-navigation">
        <button 
          className={`tab-btn ${activeTab === 'opportunity' ? 'active' : ''}`}
          onClick={() => setActiveTab('opportunity')}
        >
          🎯 Product Opportunities
        </button>
        <button 
          className={`tab-btn ${activeTab === 'weather' ? 'active' : ''}`}
          onClick={() => setActiveTab('weather')}
        >
          🌤️ Weather Assistant
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'opportunity' && (
          <div>
            <p>Discover high-potential product opportunities with AI-powered market analysis.</p>
            <ProductOpportunityChat />
          </div>
        )}
        
        {activeTab === 'weather' && (
          <div>
            <p>Chat with our weather assistant about meteorology and weather patterns.</p>
            <BedrockChat />
          </div>
        )}
      </div>
    </div>
  );
}

export default ProductDashboard;