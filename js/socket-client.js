const socket = io();

function fetchCompany() {
  const selected = document.getElementById("companySelector").value;
  if (selected) {
    // Clear old data
    document.getElementById("salesGrowth").innerText = "--";
    document.getElementById("profitGrowth").innerText = "--";
    document.getElementById("roe").innerText = "--";
    document.getElementById("prosList").innerHTML = "";
    document.getElementById("consList").innerHTML = "";

    socket.emit("send_data", { company: selected });
  }
}

socket.on("analysis_update", (data) => {
  if (data.error) {
    alert(data.error);
    return;
  }

  document.getElementById("salesGrowth").innerText = data.compounded_sales_growth || "--";
  document.getElementById("profitGrowth").innerText = data.compounded_profit_growth || "--";
  document.getElementById("roe").innerText = data.roe || "--";

  document.getElementById("prosList").innerHTML = data.pros.map(p => `<li class="green">+ ${p.trim()}</li>`).join("");
  document.getElementById("consList").innerHTML = data.cons.map(c => `<li class="red">– ${c.trim()}</li>`).join("");
});
