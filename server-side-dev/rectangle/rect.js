
const rect = {
  perimeter (x, y) {
    return 2 * (x + y);
  },

  area (x, y) {
    return x * y;
  }
};

const solveRect = (l, b) => {
  if (l < 0 || b < 0) {
    console.log('Rectangle dimensions should be greater than zero');
  } else {
    console.log(`Area: ${rect.area(l, b)}\
                 Perimeter: ${rect.perimeter(l, b)}`);
  }
}

solveRect(2, 4);
solveRect(3, 5);
solveRect(-3, 5);
