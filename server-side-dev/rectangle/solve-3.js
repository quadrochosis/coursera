const argv = require('yargs')
  .usage('Usage: node $0 --l=[num] --b=[num]')
  .demand(['l', 'b'])
  .argv;

const rect = require('./rectCb');

const solveRect = (l, b) => {
  rect(l, b, (err, rectangle) => {
    if (err) {
      console.log(err);
    } else {
      console.log(`Area: ${rectangle.area()}\
                   Perimeter: ${rectangle.area()}`);
    }
  });
}

solveRect(argv.l, argv.b);
