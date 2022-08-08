const axios = require("axios");
const fs = require("fs");
const { getSheets } = require("./getSheets.js");
const {
  docID,
  sheetID,
  credentialsPath,
  studentURLs,
  numberOfPeople,
  blackListPath,
} = require("./Constants");

var black_list_data = ['["one"]', '["two"]'];
var all_black = '["one", "two"]';
var inner_black_counter = 0;
var inner_black_array = [0, 0];

overMistake();

async function overMistake() {
  const resp = await getSheets(docID, sheetID, credentialsPath);
  var totalID = [].concat.apply([], resp); // flat double array

  for (i = 1; i < numberOfPeople + 1; i++) {
    calculate(i);
    inner_black_counter += 1;
  }

  function calculate(studentID) {
    var tmp = totalID.filter(function (value) {
      return value === String(studentID);
    });
    console.log("ID " + studentID + " has " + tmp.length + " mistake");
    if (tmp.length > 3) {
      inner_black_array[inner_black_counter] = studentID;
      // LINE notify
      axios.post(studentURLs[studentID - 1].studentURL, {
        value1: `${studentID}號，被公審超過三次還學不乖，那就一個禮拜不要用吧！`,
      });
    }
  }

  // reset
  fs.writeFile(blackListPath, '[""]', function (err) {
    if (err) throw err;
  });

  inner_black_array = inner_black_array.filter(function (item) {
    return item !== 0;
  });

  if (inner_black_array.length == 2) {
    fs.writeFile(blackListPath, all_black, function (err) {
      if (err) throw err;
      else console.log("black list update complete!!");
    });
  } else if (inner_black_array.length == 1) {
    fs.writeFile(
      blackListPath,
      black_list_data[inner_black_array[0] - 1],
      function (err) {
        if (err) throw err;
        else console.log("black list update complete!");
      }
    );
  } else console.log("no one is banned");
}
