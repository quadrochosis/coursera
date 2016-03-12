const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const hostname = 'localhost';
const port = 3000;

const app = express();

app.use(morgan('dev'));

app.use(bodyParser.json());

app.all('/dishes', (req, res, next) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });

  next();
});

app.get('/dishes', (req, res, next) => res.end('Will send all the dishes to you!'));
app.post('/dishes', (req, res, next) => res.end(`Will add the dish: ${req.body.name} with details: ${req.body.description}.`));
app.delete('/dishes', (req, res, next) => res.end('Deleting all dishes.'));
app.get('/dishes/:dishId', (req, res, next) => res.end(`Sending the details of dish: ${req.params.dishId} to you!`));
app.delete('/dishes/:dishId', (req, res, next) => res.end(`Deleting dish: ${req.params.dishId}.`));
app.put('/dishes/:dishId', (req, res, next) => {
  res.write(`Updating the dish: ${req.params.dishId}\n`);
  res.end(`Will update the dish: ${req.body.name} with details ${req.body.description}`);
});

app.use(express.static(`${__dirname}/public`));

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
