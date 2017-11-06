// Calculator
var print = document.getElementById('print');
var erase = false;

var go = function(x) {
  if (x === 'ac') {
	print.value = null;
	erase = false;
  } else if (x === 'eval') {
      print.value = Math.round(evil(print.value) * 10000) / 10000;
      erase = true;
  } else if (erase === true) {
        print.value = x;
        erase = false;
  } else {
    print.value += x;
  }
};

function evil(fn) {
  return new Function('return ' + fn)();
}

$(document).ready(function() {
    $('.my-select').select2();
});

// END
