// Import Dependencies
const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');

// Configure server options
const hostname = 'localhost';
const port = 3000;

// Generate app
const app = express();

// Import routes
const dishes = require('./routes/dishes');
const promotions = require('./routes/promotions');
const leadership = require('./routes/leadership');

// Apply middlewares
app.use(morgan('dev'));
app.use(bodyParser.json());
app.use(express.static(`${__dirname}/public`));

// Register routes
app.use('/dishes', dishes);
app.use('/promotions', promotions);
app.use('/leadership', leadership);

// Start Server
app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
