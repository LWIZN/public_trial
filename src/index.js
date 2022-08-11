var totalMoney = document.querySelector("p");

var addMoneyButton = document.querySelector("#addMoney");

var resetButton = document.querySelector("#reset");

var startButton = document.querySelector("#start");

var takeButton = document.querySelector("#take");

let moneyTMP = 0;

startButton.disabled = true;

addMoneyButton.onclick = function () {
  moneyTMP += 10;
  totalMoney.textContent = moneyTMP + " 元";
  if (moneyTMP > 20) {
    startButton.disabled = false;
  }
};

resetButton.onclick = function () {
  moneyTMP = 0;
  totalMoney.textContent = moneyTMP + " 元";
  startButton.disabled = true;
};

startButton.onclick = function () {
  $.get("http://localhost:5000/start", function (data) {
    console.log(data);
  });
  moneyTMP -= 30;
  totalMoney.textContent = moneyTMP + " 元";
  if (moneyTMP < 30) {
    startButton.disabled = true;
  }
};

takeButton.onclick = function () {
  $.get("http://localhost:5000/take_cloths", function (data) {
    console.log(data);
  });
};
