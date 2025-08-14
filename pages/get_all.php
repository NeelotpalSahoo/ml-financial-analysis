<?php
header("Content-Type: application/json");

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "ml_financial";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    echo json_encode(["error" => "❌ Connection failed"]);
    exit;
}

$result = $conn->query("SELECT company_id FROM analysis_backup ORDER BY company_id");

$companies = [];
while ($row = $result->fetch_assoc()) {
    $companies[] = $row;
}

echo json_encode($companies);
$conn->close();
