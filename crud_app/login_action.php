<?php
require_once 'functions.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $username = $_POST['username'] ?? '';
  $password = $_POST['password'] ?? '';

  if (loginUser($username, $password)) {
    header("Location: dashboard.php");
    exit;
  } else {
    echo "Invalid username or password.";
    exit;
  }
}
?>