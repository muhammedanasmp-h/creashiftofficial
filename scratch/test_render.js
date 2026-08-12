const ejs = require('ejs');
const path = require('path');
const fs = require('fs');

const viewsDir = path.join(__dirname, '..', 'views');
const dashboardPath = path.join(viewsDir, 'admin', 'dashboard.ejs');

const user = { displayName: 'Test User' };
const contents = [];

ejs.renderFile(dashboardPath, { user, contents }, (err, str) => {
    if (err) {
        console.error('EJS RENDER ERROR:', err);
    } else {
        console.log('EJS RENDER SUCCESS! Length:', str.length);
    }
});
