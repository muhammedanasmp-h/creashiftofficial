const https = require('https');

https.get('https://creashift.com/admin', (res) => {
    console.log('Status Code:', res.statusCode);
    console.log('Headers:', res.headers);
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
        console.log('Body:', body);
    });
}).on('error', (err) => {
    console.error('Error:', err);
});
