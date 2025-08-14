const socket = io();

function fetchCompany() {
  const selected = document.getElementById("companySelector").value;
  if (selected) {
    socket.emit("send_data", { company: selected });

    // Clear previous values
    document.querySelectorAll("span").forEach(el => el.innerText = "--");
    document.getElementById("prosList").innerHTML = "";
    document.getElementById("consList").innerHTML = "";
  }
}

socket.on("analysis_update", (data) => {
  if (data.error) {
    alert(data.error);
    return;
  }

  // Sales Growth
  document.getElementById("salesTTM").innerText = data.sales_growth.ttm || "--";
  document.getElementById("sales3Y").innerText = data.sales_growth["3y"] || "--";
  document.getElementById("sales5Y").innerText = data.sales_growth["5y"] || "--";
  document.getElementById("sales10Y").innerText = data.sales_growth["10y"] || "--";

  // Profit Growth
  document.getElementById("profitTTM").innerText = data.profit_growth.ttm || "--";
  document.getElementById("profit3Y").innerText = data.profit_growth["3y"] || "--";
  document.getElementById("profit5Y").innerText = data.profit_growth["5y"] || "--";
  document.getElementById("profit10Y").innerText = data.profit_growth["10y"] || "--";

  // ROE
  document.getElementById("roeTTM").innerText = data.roe.ttm || "--";
  document.getElementById("roe3Y").innerText = data.roe["3y"] || "--";
  document.getElementById("roe5Y").innerText = data.roe["5y"] || "--";
  document.getElementById("roe10Y").innerText = data.roe["10y"] || "--";

  // Pros
  document.getElementById("prosList").innerHTML = data.pros.map(p => `<li class="green">+ ${p.trim()}</li>`).join("");

  // Cons
  document.getElementById("consList").innerHTML = data.cons.map(c => `<li class="red">– ${c.trim()}</li>`).join("");
});

fetch(`/predict/${company}`)
  .then(response => response.json())
  .then(data => {
    document.getElementById("predictedSales").innerText = `Expected Sales Growth: ${data.predicted_growth}%`;
  });
