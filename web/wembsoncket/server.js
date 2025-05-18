// server.js
const express = require('express');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const http = require('http');
const WebSocket = require('ws'); // WebSocket library
const fs = require('fs');
const { visitUrl } = require('./adminBot'); // Import the visitUrl function

const app = express();
const port = 3000;

// Secret key for signing JWT
const JWT_SECRET = fs.readFileSync('secret.txt', 'utf8').trim()
const FLAG = fs.readFileSync('flag.txt', 'utf8').trim()

// Middleware to parse cookies
app.use(cookieParser());

// Create HTTP server
const server = http.createServer(app);

// Create a WebSocket server
const wss = new WebSocket.Server({ server });

// Middleware to check for a valid JWT cookie
const checkCookie = (req, res, next) => {
  const token = req.cookies.token;

  // If the user does not have a token, generate a new one
  if (!token) {
    const userId = uuidv4();
    const jwtToken = jwt.sign({ userId }, JWT_SECRET);
    res.cookie('token', jwtToken, {
      httpOnly: true,
      sameSite: 'None',
      secure: true
    });
    return res.redirect('/');
  }

  try {
    // Verify the JWT token and get the userId
    const decoded = jwt.verify(token, JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (error) {
    // If the JWT token is invalid, generate a new one
    const userId = uuidv4();
    const jwtToken = jwt.sign({ userId }, JWT_SECRET);
    res.cookie('token', jwtToken, {
      httpOnly: true,
      sameSite: 'None',
      secure: true
    });
    return res.redirect('/');
  }
};

// Send a message to the WebSocket
const sendMsg = (ws, msg) => {
  ws.send(JSON.stringify({ message: msg, sender: 'URL Bot' }));
};

// Serve the static files after checking the cookie
app.get('/', checkCookie, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// WebSocket connection handler
wss.on('connection', (ws, req) => {
  // Get the userId from the cookie
  const userId = req.headers.cookie ? req.headers.cookie.split('token=')[1] : null;

  if (userId) {
    try {
      const decoded = jwt.verify(userId, JWT_SECRET);
      const user = decoded.userId;

      sendMsg(ws, `Welcome! Send a URL and the admin will visit it to check if it's up`);

      ws.on('message', async (data) => {
        try {
          const message = JSON.parse(data);

          if (message.message === '/getFlag') {
            if (user === 'admin') {
              sendMsg(ws, `Flag: ${FLAG}`);
            } else {
              sendMsg(ws, 'You are not authorized to get the flag');
            }
          } else {
            if (message.message.startsWith('http://') || message.message.startsWith('https://')) {
              sendMsg(ws, 'Checking URL...');
              const result = await visitUrl(message.message); // have the adminBot visit the URL
              if (result === 'success') {
                sendMsg(ws, `${message.message} is up!`);
              } else {
                sendMsg(ws, `${message.message} returned an error: ${result}`);
              }
            } else {
              sendMsg(ws, 'Please send a URL starting with http:// or https://');
            }
          }
        } catch (error) {
          // Invalid message
          ws.close();
        }
      });
    } catch (error) {
      // Invalid JWT
      ws.close();
    }
  } else {
    // No userId found in the cookie
    ws.close();
  }
});

// Start the HTTP server
server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});