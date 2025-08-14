<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>All Financial Data</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div class="container mt-5">
    <h2 class="mb-4 text-center">📊 All Financial Data</h2>

    <?php
    $conn = new mysqli("localhost", "root", "", "ml_financial");

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $sql = "SELECT * FROM financial_data ORDER BY company_id";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        echo '<table class="table table-bordered table-hover">';
        echo '<thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Company ID</th>
                    <th>Cash Flow</th>
                    <th>Profit & Loss</th>
                    <th>Balance Sheet</th>
                    <th>Created At</th>
                </tr>
              </thead><tbody>';
        while($row = $result->fetch_assoc()) {
            echo '<tr>';
            echo '<td>' . $row["id"] . '</td>';
            echo '<td>' . $row["company_id"] . '</td>';
            echo '<td><pre>' . htmlspecialchars($row["cash_flow"]) . '</pre></td>';
            echo '<td><pre>' . htmlspecialchars($row["profit_loss"]) . '</pre></td>';
            echo '<td><pre>' . htmlspecialchars($row["balance_sheet"]) . '</pre></td>';
            echo '<td>' . $row["created_at"] . '</td>';
            echo '</tr>';
        }
        echo '</tbody></table>';
    } else {
        echo "<div class='alert alert-info'>No financial data found.</div>";
    }

    $conn->close();
    ?>
  </div>
</body>
</html>