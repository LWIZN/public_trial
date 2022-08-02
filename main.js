const axios = require("axios");
const { getSheets } = require("./getSheets.js");
const {
  docID,
  sheetID,
  credentialsPath,
  studentURLs,
  numberOfPeople,
} = require("./Constants");

(async () => {
  const resp = await getSheets(docID, sheetID, credentialsPath);
  var totalID = [].concat.apply([], resp); // flat double array

  for (i = 1; i < numberOfPeople + 1; i++) {
    calculate(i);
  }

  function calculate(studentID) {
    var tmp = totalID.filter(function (value) {
      return value === String(studentID);
    });

    console.log("ID " + studentID + ": has " + tmp.length + " mistake");
    if (tmp.length > 3) {
      // LINE notify
      axios.post(studentURLs[studentID - 1].studentURL, {
        value1: "被公審超過三次還學不乖，那就一個禮拜不要用吧！",
      });
    }
  }
})();
