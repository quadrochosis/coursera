// Import dependencies
const express = require('express');

// Leadership route
const leadership = express.Router();
leadership.route('/')
.all((req, res, next) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });

  next();
})
.get((req, res, next) => res.end('Will send all the leaders to you'))
.post((req, res, next) => res.end(`Will add leader ${req.body.name} with details: ${req.body.description}.`))
.delete((req, res, next) => res.end('Deleting all leaders'));

leadership.route('/:leaderId')
.all((req, res, next) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });

  next();
})
.get((req, res, next) => res.end(`Sending data for leader ${req.body.name}.`))
.put((req, res, next) => res.end(`Updating leader ${req.body.name} [${req.params.leaderId}] with details: ${req.body.description}.`))
.delete((req, res, next) => res.end(`Deleting leader ${req.params.leaderId}.`));

module.exports = leadership;
