require('dotenv').config();
const express = require('express');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');
const cors = require('cors');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname)); // Serve existing static files

// Database Connection
const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
});

// Test DB Connection
pool.connect((err, client, release) => {
    if (err) {
        return console.error('Error acquiring client', err.stack);
    }
    console.log('Connected to Database');
    release();
});

// API Routes

// Register (Admin Only - Self Registration)
app.post('/api/auth/register', async (req, res) => {
    const { username, password, role, fullName } = req.body;

    if (!username || !password || !role) {
        return res.status(400).json({ error: 'Missing fields' });
    }

    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const result = await pool.query(
            'INSERT INTO users (username, password_hash, role, full_name) VALUES ($1, $2, $3, $4) RETURNING id, username, role',
            [username, hashedPassword, role, fullName]
        );
        res.status(201).json(result.rows[0]);
    } catch (err) {
        console.error(err);
        if (err.code === '23505') { // Unique violation
            return res.status(409).json({ error: 'Username already exists' });
        }
        res.status(500).json({ error: 'Server error' });
    }
});

// Create User (Admin Action - Generate Credentials)
app.post('/api/admin/create-user', async (req, res) => {
    const { name, role, dob } = req.body;

    if (!name || !role || !dob) {
        return res.status(400).json({ error: 'Missing fields: name, role, dob' });
    }

    // Generate Credentials
    // Username: name in small (remove spaces)
    const username = name.toLowerCase().replace(/\s+/g, '');
    // Password: dob (format preserved from input, typically YYYY-MM-DD)
    const password = dob;

    try {
        const hashedPassword = await bcrypt.hash(password, 10);

        const result = await pool.query(
            'INSERT INTO users (username, password_hash, role, full_name) VALUES ($1, $2, $3, $4) RETURNING id, username, role',
            [username, hashedPassword, role, name]
        );

        // Return the generated credentials so Admin knows (optional but helpful)
        res.status(201).json({
            message: 'User created successfully',
            user: result.rows[0],
            generatedCredentials: { username, password }
        });

    } catch (err) {
        console.error(err);
        if (err.code === '23505') {
            // Append random digits if username exists? Or just error.
            // For now error, but in prod we'd handle duplicates.
            return res.status(409).json({ error: `Username '${username}' already exists. Please use a distinct name or handle duplicates.` });
        }
        res.status(500).json({ error: 'Server error' });
    }
});


// Login
app.post('/api/auth/login', async (req, res) => {
    const { username, password, role } = req.body;

    try {
        const result = await pool.query('SELECT * FROM users WHERE username = $1 AND role = $2', [username, role]);

        if (result.rows.length === 0) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        const user = result.rows[0];
        const validPassword = await bcrypt.compare(password, user.password_hash);

        if (!validPassword) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        // Return user info (excluding password)
        res.json({
            id: user.id,
            username: user.username,
            role: user.role,
            name: user.full_name
        });

    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error' });
    }
});

app.get('*', (req, res) => {
    if (!req.path.includes('.')) {
        res.sendFile(path.join(__dirname, 'login.html'));
    } else {
        res.status(404).end();
    }
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
