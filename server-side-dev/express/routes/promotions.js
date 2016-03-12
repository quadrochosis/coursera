// Import dependencies
const express = require('express');

// Promotion route
const promotions = express.Router();
promotions.route('/')
.all((req, res, next) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });

  next();
})
.get((req, res, next) => res.end('Will send all the promotions to you'))
.post((req, res, next) => res.end(`Will add promotion ${req.body.name} with details: ${req.body.description}.`))
.delete((req, res, next) => res.end('Deleting all promotions'));

promotions.route('/:promoId')
.all((req, res, next) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });

  next();
})
.get((req, res, next) => res.end(`Sending data for promotion ${req.body.name}.`))
.put((req, res, next) => res.end(`Updating promo ${req.body.name} [${req.params.promoId}] with details: ${req.body.description}.`))
.delete((req, res, next) => res.end(`Deleting promot ${req.params.promoId}.`));

module.exports = promotions;
