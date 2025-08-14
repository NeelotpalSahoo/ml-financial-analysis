<?php
// Set headers
header("Content-Type: text/html");

// Your API config
$api_key = "ghfkffu6378382826hhdjgk";
$company_id = isset($_GET['id']) ? strtoupper($_GET['id']) : null;
$return_json = isset($_GET['json']) && $_GET['json'] == "1";

// Validate company ID
if (!$company_id) {
    $error = ["error" => "No company ID provided"];
    echo $return_json ? json_encode($error) : "<h2>❌ No company ID provided.</h2>";
    exit;
}

// API URL
$url = "https://bluemutualfund.in/server/api/company.php?id={$company_id}&api_key={$api_key}";

// Fetch the API response
$response = file_get_contents($url);

// Handle fetch error
if (!$response) {
    $error = ["error" => "API request failed"];
    echo $return_json ? json_encode($error) : "<h2>❌ Failed to fetch data from API.</h2>";
    exit;
}

// Decode the JSON response
$data = json_decode($response, true);

// Handle decode error
if (!$data || !isset($data['company'])) {
    $error = ["error" => "Invalid API response"];
    echo $return_json ? json_encode($error) : "<h2>❌ Invalid API response format.</h2>";
    exit;
}

// Extract data
$company = $data['company'];
$cashflow = $data['data']['cashflow'] ?? [];
$balancesheet = $data['data']['balancesheet'] ?? [];
$profitandloss = $data['data']['profitandloss'] ?? [];
$analysis = $data['data']['analysis'] ?? [];
$prosandcons = $data['data']['prosandcons'][0] ?? ['pros' => '', 'cons' => ''];

// Format pros and cons
$pros = array_filter(array_map('trim', explode("\n", $prosandcons['pros'] ?? '')));
$cons = array_filter(array_map('trim', explode("\n", $prosandcons['cons'] ?? '')));

// Output JSON if requested
if ($return_json) {
    echo json_encode([
        "company" => $company,
        "pros" => $pros,
        "cons" => $cons,
        "cashflow" => $cashflow,
        "balancesheet" => $balancesheet,
        "profitandloss" => $profitandloss,
        "analysis" => $analysis,
    ]);
    exit;
}

// Otherwise display basic HTML
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title><?php echo $company['company_name']; ?> – Company Analysis</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { padding: 30px; background-color: #f8f9fa; }
    .card { margin-bottom: 20px; }
    .logo { height: 60px; margin-bottom: 10px; }
    ul { padding-left: 1rem; }

    .company-logo {
  width: 100px;
  height: 100px;
  object-fit: contain;
  border-radius: 50%;
  display: block;
  margin: 0 auto;
  border: 2px solid #ccc;
}
  </style>
</head>
<body>
  <div class="container">
    <h1 class="text-center mb-4"><?php echo htmlspecialchars($company['company_name']); ?></h1>
    <div class="text-center mb-4">
        <?php
        $logo_path = "../assets/logos/{$company_id}.png";
          if (file_exists($logo_path)) {
            echo "<img src='{$logo_path}' class='logo' alt='Logo'>";
          } else {
            echo "<div class='text-muted'>No logo available</div>";
          }
          ?>

    </div>
    <p class="lead"><?php echo htmlspecialchars($company['about_company']); ?></p>

    <div class="row">
      <!-- Pros -->
      <div class="col-md-6">
        <div class="card border-success shadow-sm">
          <div class="card-header bg-success text-white">✅ Pros</div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <?php
              foreach ($pros as $p) {
                  echo "<li class='list-group-item'>" . htmlspecialchars($p) . "</li>";
              }
              ?>
            </ul>
          </div>
        </div>
      </div>

      <!-- Cons -->
      <div class="col-md-6">
        <div class="card border-danger shadow-sm">
          <div class="card-header bg-danger text-white">⚠️ Cons</div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <?php
              foreach ($cons as $c) {
                  echo "<li class='list-group-item'>" . htmlspecialchars($c) . "</li>";
              }
              ?>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-4">
      <a href="view_all.html" class="btn btn-secondary">← Back to All Companies</a>
    </div>
  </div>
</body>
</html>
