var totalMoney = document.querySelector("p");

var addMoneyButton = document.querySelector("#addMoney");

var resetButton = document.querySelector("#reset");

var startButton = document.querySelector("#start");

let moneyTMP = 0;

addMoneyButton.onclick = function () {
  moneyTMP += 10;
  totalMoney.textContent = moneyTMP + " 元";
};

resetButton.onclick = function () {
  moneyTMP = 0;
  totalMoney.textContent = moneyTMP + " 元";
};

startButton.onclick = function () {
  $.get("http://localhost:5000/home/start", function (data) {
    console.log(data);
  });
};

takeButton.onclick = function () {
  $.get("http://localhost:5000/take_cloths", function (data) {
    console.log(data);
  });
};
