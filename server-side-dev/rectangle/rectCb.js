module.exports = (x, y, next) => {
  try {
    if (x < 0 || y < 0) {
      throw new Error('Rectangle dimensions should be greater than zero.');
    } else {
      return next(null, {
        perimeter() {
          return 2 * (x + y);
        },

        area() {
          return x * y;
        }
      });
    }
  }

  catch(err) {
    return next(err);
  }
}
