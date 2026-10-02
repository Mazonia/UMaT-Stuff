<?php
// Enable error reporting for debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Include the functions file
require_once 'functions.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST['name'] ?? '';
  $email = $_POST['email'] ?? '';
  $username = $_POST['username'] ?? '';
  $password = $_POST['password'] ?? '';
  $confirm_password = $_POST['confirm_password'] ?? '';

  // Validate form data
  if (empty($name) || empty($email) || empty($username) || empty($password) || empty($confirm_password)) {
    echo "All fields are required.";
    exit;
  }

  if ($password !== $confirm_password) {
    echo "Passwords do not match.";
    exit;
  }

  if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "Invalid email format.";
    exit;
  }

  // Check if username or email already exists
  $stmt = $conn->prepare("SELECT * FROM users WHERE username = ? OR email = ?");
  $stmt->bind_param("ss", $username, $email);
  $stmt->execute();
  $result = $stmt->get_result();

  if ($result->num_rows > 0) {
    echo "Username or email already exists.";
    exit;
  }

  // Register the user
  if (registerUser($name, $email, $username, $password)) {
    header("Location: login.php");
    exit;
  } else {
    echo "Error registering user: " . $conn->error;
    exit;
  }
}
?>