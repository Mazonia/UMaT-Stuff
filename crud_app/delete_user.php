<?php
require_once 'functions.php';

$id = $_GET['id']?? '';

if (!empty($id) && deleteUser($id)) {
  header("Location: dashboard.php");
  exit;
} else {
  echo "Error deleting user.";
  exit;
}
?>