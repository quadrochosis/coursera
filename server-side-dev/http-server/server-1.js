const http = require('http');

// Configure
const hostname = 'localhost';
const port = 3000;

// Create Server
const server = http.createServer((req, res) => {
  // Print headers
  console.log(req.headers);

  // Construct Response
  res.writeHead(200, { 'Content-Type': 'text/html' });

  if (req.headers['postman-token']) {
    res.write('<h1>Sneaky Postman :P</h1>');
  }

  res.end('<h1>Hello World!</h1>');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
