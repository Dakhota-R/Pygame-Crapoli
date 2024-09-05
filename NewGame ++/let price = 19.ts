let price = 19.5;
let cid = [
  ['PENNY', .5],
  ['NICKEL', 0],
  ['DIME', 0],
  ['QUARTER', 0],
  ['ONE', 0],
  ['FIVE', 0],
  ['TEN', 0],
  ['TWENTY', 0],
  ['ONE HUNDRED', 0]
];

const cashInput = document.getElementById("cash");
const priceElement = document.getElementById("price");
const changeDrawerElement = document.getElementById("change-in-drawer");
const purchaseBtn = document.getElementById("purchase-btn");
const changeDueElement = document.getElementById("change-due");

const setPriceElement = () => {priceElement.innerText = price};

const setCashInDrawer = (arr) => {
  arr.forEach((currencyArr) => {
    changeDrawerElement.innerHTML += `
    <span>${currencyArr[0]}: ${currencyArr[1]}</span>
    `
  })
}

let possible = true;

let change = {}


const denominations = [
  ["PENNY", .01],
  ["NICKEL", .05],
  ["DIME", .10],
  ["QUARTER", .25],
  ["ONE", 1],
  ["FIVE", 5],
  ["TEN", 10],
  ["TWENTY", 20],
  ["ONE HUNDRED", 100]
]

const getUsedBills = (available, needed) => {
  let used;
  if (available >= needed) {
    used = needed;
  } else {
    used = available;
  };
  return used;
}

const reduceCID = (cashDrawer) => {
  const reduced = cashDrawer.map((x) => x[1]).reduce((acc, val) => acc + val, 0);
  return reduced;
}

//////////////////////////////////////////////////////////
let status = "OPEN";

const getChangeTest = (payment) => {
  let changeDue = Math.round((payment - price) * 100) / 100;
  const denomList = denominations.reverse();
  for (const d in cid.reverse()) {
    if (changeDue > 0) {
      const denom = denomList[d][1]; 
      const available = Math.round(cid[d][1] / denom);
      const needed = Math.floor(changeDue / denom);
      const usedBills = getUsedBills(available, needed);

      changeDue = Math.round((changeDue - usedBills * denom) * 100) / 100;
      console.log(changeDue)

      // adjust CID
      cid[d][1] = cid[d][1] - usedBills * denom;
      change[cid[d][0]] = usedBills * denom;

      if (reduceCID(cid) == 0){
        status = "CLOSED";
      }
    }
  }
  if (changeDue != 0) {
    status = "INSUFFICIENT_FUNDS"
  }
}

/////////////////////////////////////////////////////////////////
const getChange = (payment) => {
  change = {};
  getChangeTest(payment);

  if (payment < price) {
    alert("Customer does not have enough money to purchase the item");
  };
  if (payment == price) {
    changeDueElement.innerText = "No change due - customer paid with exact cash";
    return;
  };
  if (status == "CLOSED" || status == "OPEN"){
    for (const ele in change) {
      if (change[ele] != 0){
        status += `\n${ele}: $${change[ele]}`
      }
    }
  }
  changeDueElement.innerText = "Status: " + status;
  console.log(changeDueElement.innerText)
}


setPriceElement();
setCashInDrawer(cid);

purchaseBtn.addEventListener("click", () => {
  getChange(Number(cashInput.value));
})