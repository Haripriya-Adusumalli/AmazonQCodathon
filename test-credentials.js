// Test script to verify AWS credentials
import { Amplify } from 'aws-amplify';
import { fetchAuthSession } from 'aws-amplify/auth';
import { awsConfig } from './src/aws-config.js';

Amplify.configure(awsConfig);

async function testCredentials() {
  try {
    console.log('Testing AWS credentials...');
    
    const session = await fetchAuthSession({ forceRefresh: true });
    
    if (session.credentials) {
      console.log('✅ Credentials found:');
      console.log('Access Key ID:', session.credentials.accessKeyId);
      console.log('Session Token exists:', !!session.credentials.sessionToken);
      console.log('Identity ID:', session.identityId);
    } else {
      console.log('❌ No credentials available');
    }
    
  } catch (error) {
    console.error('❌ Error:', error);
  }
}

testCredentials();