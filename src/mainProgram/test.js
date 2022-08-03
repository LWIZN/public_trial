const fs = require("fs");

black_list_data = ['["one"]', '["two"]'];
all_black = '["one", "two"]';

fs.readFile("./src/black_list_tmp.json", function (err, data) {
  if (err) throw err;
  else if (data.toString() == black_list_data[1] || data.toString() == "") {
    fs.writeFile(
      "./src/black_list_tmp.json",
      black_list_data[1],
      function (err) {
        if (err) throw err;
        else console.log("black list update complete");
      }
    );
  } else {
    fs.writeFile("./src/black_list_tmp.json", all_black, function (err) {
      if (err) throw err;
      else console.log("black list update complete");
    });
  }
});

var testArry = [];
var counter = 0;
for (i = 0; i < 9; i++) {
  testArry[counter] = i;
  counter += 1;
}

testArry = testArry.filter(function (item) {
  return item !== 1;
});

console.log(testArry);
