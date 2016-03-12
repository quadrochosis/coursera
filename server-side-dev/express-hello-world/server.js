const express = require('express');
const morgan = require('morgan');

const hostname = 'localhost';
const port = 3000;

const app = express();

app.use(morgan('dev'));

app.use(express.static(`${__dirname}/public`));

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
