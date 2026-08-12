const ejs = require('ejs');
const path = require('path');

const viewsDir = path.join(__dirname, '..', 'views');
const dashboardPath = path.join(viewsDir, 'admin', 'dashboard.ejs');

const testCases = [
    { name: 'Valid User', data: { user: { displayName: 'John Doe' }, contents: [] } },
    { name: 'User without displayName', data: { user: { email: 'john@example.com' }, contents: [] } },
    { name: 'Null User', data: { user: null, contents: [] } },
    { name: 'Undefined User', data: { contents: [] } }
];

testCases.forEach(tc => {
    ejs.renderFile(dashboardPath, tc.data, (err, str) => {
        if (err) {
            console.error(`TEST [${tc.name}] FAILED:`, err.message);
        } else {
            console.log(`TEST [${tc.name}] PASSED! Output length: ${str.length}`);
        }
    });
});
