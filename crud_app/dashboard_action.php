<?php
require_once 'functions.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $id = $_POST['id'] ?? '';
  $name = $_POST['name'] ?? '';
  $email = $_POST['email'] ?? '';
  $username = $_POST['username'] ?? '';
  $password = $_POST['password'] ?? '';
  $confirm_password = $_POST['confirm_password'] ?? '';

  if ($password !== $confirm_password || empty($password)) {
    echo "Passwords do not match.";
    exit;
  }

  if (updateUser($id, $name, $email, $username, $password)) {
    header("Location: dashboard.php");
    exit;
  } else {
    echo "Error updating user.";
    exit;
  }
}
?>