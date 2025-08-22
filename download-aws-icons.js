const https = require('https');
const fs = require('fs');
const path = require('path');

// Create icons directory
if (!fs.existsSync('aws-icons')) {
    fs.mkdirSync('aws-icons');
}

// Official AWS Architecture Icons URLs
const icons = {
    'amplify': 'https://icon.icepanel.io/AWS/svg/Front-End-Web-Mobile/Amplify.svg',
    'cognito': 'https://icon.icepanel.io/AWS/svg/Security-Identity-Compliance/Cognito.svg',
    'bedrock': 'https://icon.icepanel.io/AWS/svg/Machine-Learning/Bedrock.svg',
    'lambda': 'https://icon.icepanel.io/AWS/svg/Compute/Lambda.svg',
    'user': 'https://icon.icepanel.io/Technology/svg/User.svg'
};

function downloadIcon(name, url) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(`aws-icons/${name}.svg`);
        https.get(url, (response) => {
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                console.log(`Downloaded ${name}.svg`);
                resolve();
            });
        }).on('error', (err) => {
            fs.unlink(`aws-icons/${name}.svg`, () => {});
            console.error(`Error downloading ${name}: ${err.message}`);
            reject(err);
        });
    });
}

async function downloadAllIcons() {
    console.log('Downloading official AWS service icons...');
    
    for (const [name, url] of Object.entries(icons)) {
        try {
            await downloadIcon(name, url);
        } catch (error) {
            console.error(`Failed to download ${name}`);
        }
    }
    
    console.log('Icon download complete!');
}

downloadAllIcons();