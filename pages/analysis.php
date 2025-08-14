<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Real-Time Company Analysis</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <style>
    body { padding: 20px; background-color: #f8f9fa; }
    .pros { background-color: #d4edda; padding: 15px; border-radius: 5px; }
    .cons { background-color: #f8d7da; padding: 15px; border-radius: 5px; }
  </style>
</head>
<body>
  <div class="container">
    <h2> Live Company Analysis</h2>
    <input type="text" id="companyInput" class="form-control" placeholder="Enter Company ID (e.g. TCS)">
    <button onclick="fetchAnalysis()" class="btn btn-primary mt-2">Fetch Analysis</button>

    <div id="result" class="mt-4"></div>
  </div>

  <script>
    function fetchAnalysis() {
      const companyId = document.getElementById("companyInput").value.trim();
      if (!companyId) return alert("Please enter a company ID");

      const url = `http://127.0.0.1:5000/api/analysis/${companyId}`;
      fetch(url)
        .then(res => res.json())
        .then(data => {
          if (data.error) {
            document.getElementById("result").innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
          } else {
            const pros = data.pros.split("\n").map(p => `<li>${p}</li>`).join("");
            const cons = data.cons.split("\n").map(c => `<li>${c}</li>`).join("");
            document.getElementById("result").innerHTML = `
              <div class="pros"><h5>✅ Pros</h5><ul>${pros}</ul></div>
              <div class="cons mt-3"><h5>⚠️ Cons</h5><ul>${cons}</ul></div>
            `;
          }
        })
        .catch(err => {
          document.getElementById("result").innerHTML = `<div class="alert alert-danger">Fetch error</div>`;
          console.error("API error:", err);
        });
    }

    // Optional: Auto-refresh every 15 seconds
    setInterval(() => {
      const val = document.getElementById("companyInput").value.trim();
      if (val) fetchAnalysis();
    }, 15000);
  </script>
</body>
</html>
