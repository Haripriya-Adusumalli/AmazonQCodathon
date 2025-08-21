import { Amplify } from 'aws-amplify';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { awsConfig } from './aws-config';
import ProductDashboard from './ProductDashboard';
import './App.css';

// Configure Amplify with Identity Pool
Amplify.configure({
  ...awsConfig,
  Auth: {
    ...awsConfig.Auth,
    Cognito: {
      ...awsConfig.Auth.Cognito,
      allowGuestAccess: false
    }
  }
});

function App() {
  return (
    <div className="app">
      <Authenticator>
        {({ signOut, user }) => (
          <ProductDashboard user={user} onLogout={signOut} />
        )}
      </Authenticator>
    </div>
  );
}

export default App;