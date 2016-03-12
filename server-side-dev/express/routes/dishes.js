// Import dependencies
const express = require('express');

// Dish route
const dishes = express.Router();
dishes.route('/')
.all((req, res, next) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });

  next();
})
.get((req, res, next) => res.end('Will send all the dishes to you'))
.post((req, res, next) => res.end(`Will add dish ${req.body.name} with details: ${req.body.description}.`))
.delete((req, res, next) => res.end('Deleting all dishes'));

dishes.route('/:dishId')
.all((req, res, next) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });

  next();
})
.get((req, res, next) => res.end(`Sending data for dish ${req.body.name}.`))
.put((req, res, next) => res.end(`Updating dish ${req.body.name} [${req.params.dishId}] with details: ${req.body.description}.`))
.delete((req, res, next) => res.end(`Deleting dish ${req.params.dishId}.`));

module.exports = dishes;
