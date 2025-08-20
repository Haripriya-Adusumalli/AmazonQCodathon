import BedrockChat from './BedrockChat';

function Dashboard({ user, onLogout }) {
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome back, {user?.username || user?.signInDetails?.loginId}! 👋</h1>
        <button className="logout-btn" onClick={onLogout}>Sign Out</button>
      </div>
      <p>You have successfully authenticated with Amazon Cognito.</p>
      <BedrockChat />
    </div>
  );
}

export default Dashboard;