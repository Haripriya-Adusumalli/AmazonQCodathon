#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Product Opportunity Recommendation System - Test Suite');
console.log('=========================================================\n');

// Check if test files exist
const testDir = path.join(__dirname, 'src', '__tests__');
const testFiles = [
  'chatbot-integration.test.js',
  'backend-integration.test.js', 
  'lambda-functions.test.js'
];

console.log('📋 Checking test files...');
testFiles.forEach(file => {
  const filePath = path.join(testDir, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file} - Found`);
  } else {
    console.log(`❌ ${file} - Missing`);
  }
});

console.log('\n🧪 Running Test Suite...\n');

try {
  // Run all tests
  console.log('1️⃣ Running Frontend Chatbot Integration Tests...');
  execSync('npm run test:chatbots', { stdio: 'inherit' });
  
  console.log('\n2️⃣ Running Backend Integration Tests...');
  execSync('npm run test:backend', { stdio: 'inherit' });
  
  console.log('\n3️⃣ Running Lambda Function Tests...');
  execSync('npm run test:lambda', { stdio: 'inherit' });
  
  console.log('\n📊 Generating Coverage Report...');
  execSync('npm run test:coverage', { stdio: 'inherit' });
  
  console.log('\n✅ All tests completed successfully!');
  console.log('\n📈 Test Summary:');
  console.log('- Weather Assistant: Frontend + Backend integration');
  console.log('- Product Opportunity Analyzer (Basic): Frontend + Backend integration');
  console.log('- Enhanced Product Analyzer: Frontend + Backend + Lambda integration');
  console.log('- Lambda Functions: Unit tests for all analysis functions');
  
} catch (error) {
  console.error('\n❌ Test execution failed:', error.message);
  process.exit(1);
}