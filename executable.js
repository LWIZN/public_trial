const axios = require("axios");
const { getSheets } = require("./getSheets.js");
const {
  docID,
  sheetID,
  credentialsPath,
  student1URL,
  student2URL,
} = require("./Constants");

async function calculate() {
  const resp = await getSheets(docID, sheetID, credentialsPath);

  var totalID = [].concat.apply([], resp); // flat double array

  var student1ID = totalID.filter(function (value) {
    return value === "1";
  });

  console.log("student1ID = " + student1ID.length);
  if (student1ID.length > 3) {
    // LINE notify
    axios.post(student1URL, {
      value1: "被公審超過三次還學不乖，那就一個禮拜不要用吧！",
    });
  }

  var student2ID = totalID.filter(function (value) {
    return value === "2";
  });

  console.log("student2ID = " + student2ID.length);
  if (student2ID.length > 3) {
    axios.post(student2URL, {
      value1: "被公審超過三次還學不乖，那就一個禮拜不要用吧！",
    });
  }
}

calculate();
