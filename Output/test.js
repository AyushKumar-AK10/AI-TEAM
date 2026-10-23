const fs = require('fs');
const path = require('path');

console.log('Running automated acceptance checks...');

// AC-1 & AC-2 Check: Verify index.html exists and contains the required H1 heading
try {
  const indexPath = path.join(__dirname, 'index.html');
  if (!fs.existsSync(indexPath)) {
    console.error('FAIL: index.html does not exist.');
    process.exit(1);
  }

  const htmlContent = fs.readFileSync(indexPath, 'utf8');
  
  if (!htmlContent.includes('<h1>Hello, World!</h1>')) {
    console.error('FAIL: index.html does not contain <h1>Hello, World!</h1>');
    process.exit(1);
  }
  console.log('PASS: index.html contains <h1>Hello, World!</h1>');

  // Check stylesheet link
  if (!htmlContent.includes('rel="stylesheet"') || !htmlContent.includes('styles.css')) {
    console.error('FAIL: styles.css is not linked properly in index.html');
    process.exit(1);
  }
  console.log('PASS: styles.css is correctly referenced in index.html');

  const cssPath = path.join(__dirname, 'styles.css');
  if (!fs.existsSync(cssPath)) {
    console.error('FAIL: styles.css does not exist.');
    process.exit(1);
  }
  console.log('PASS: styles.css exists.');

  console.log('All automated acceptance tests passed successfully!');
  process.exit(0);
} catch (error) {
  console.error('FAIL: Unexpected error during testing:', error);
  process.exit(1);
}
