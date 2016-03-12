
const rect = require('./rectCb');

const solveRect = (l, b) => {
  rect(l, b, (err, rectangle) => {
    if (err) {
      console.log(err);
    } else {
      console.log(`Area: ${rectangle.area()}\
                   Perimeter: ${rectangle.perimeter()}`);
    }
  });
}

solveRect(2, 3);
solveRect(5, 5);
solveRect(-3, 5);
