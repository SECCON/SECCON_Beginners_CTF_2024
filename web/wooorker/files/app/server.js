const express = require('express');
const jwt = require('jsonwebtoken');
const path = require('path');
const crypto = require('crypto');

const app = express();
app.use(express.json());
app.use(express.static('public'));

const jwtSecret = crypto.randomBytes(64).toString('hex');
const FLAG = process.env.FLAG;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;

const users = {
  admin: { password: ADMIN_PASSWORD, isAdmin: true },
  guest: { password: 'guest', isAdmin: false }
};

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = users[username];

  if (user && user.password === password) {
    const token = jwt.sign({ username, isAdmin: user.isAdmin }, jwtSecret, { expiresIn: '1h' });
    res.status(200).json({ token });
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'flag.html'));
});

app.get('/flag', (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  try {
    const decoded = jwt.verify(token, jwtSecret);
    if (decoded.isAdmin) {
      const flag = FLAG;
      res.status(200).json({ flag });
    } else {
      res.status(403).json({ error: 'Access denied' });
    }
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
});

// レポート機能
// Redis
const Redis = require("ioredis");
let redisClient = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
});
redisClient.set("queued_count", 0);
redisClient.set("proceeded_count", 0);

app.get("/report", async (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'report.html'));
});

app.post("/report", async (req, res, next) => {
  // Parameter check
  const { path } = req.body;
  if (!path || path === "") {
    res.status(400).json({ error: 'Invalid request' });
  }
  try {
    // Enqueued jobs are processed by crawl.js
    redisClient
      .rpush("query", path)
      .then(() => {
        redisClient.incr("queued_count");
      })
      .then(() => {
        console.log("Report enqueued :", path);
        res.status(200).json({ message: 'OK. Admin will check the URL you sent.' });
      });
  } catch (e) {
    console.log("Report error :", e);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

const PORT = process.env.PORT || 34466;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
