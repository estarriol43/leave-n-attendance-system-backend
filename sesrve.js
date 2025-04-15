const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());  // To parse JSON request bodies

// Test route
app.get('/', (req, res) => {
    res.send('Leave & Attendance System API');
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
