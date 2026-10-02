<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Edit User</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <h1 class="text-center mb-4">Edit User</h1>
    <?php
    require_once 'functions.php';
    $id = $_GET['id']?? '';
    $result = getAllUsers();
    $user = null;

    if (!empty($id)) {
      foreach ($result as $u) {
        if ($u['id'] == $id) {
          $user = $u;
          break;
        }
      }
    }

    if (!$user) {
      echo "<div class='alert alert-danger'>User not found.</div>";
      exit;
    }
   ?>
    <form action="dashboard_action.php" method="post">
      <input type="hidden" name="id" value="<?php echo $user['id'];?>">
      <div class="mb-3">
        <label for="name" class="form-label">Name:</label>
        <input type="text" class="form-control" id="name" name="name" value="<?php echo $user['name'];?>" required>
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input type="email" class="form-control" id="email" name="email" value="<?php echo $user['email'];?>" required>
      </div>
      <div class**username" class="form-label">Username:</label>
        <input type="text" class="form-control" id="username" name="username" value="<?php echo $user['username'];?>" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">New Password (leave blank if no change):</label>
        <input type="password" class="form-control" id="password" name="password">
      </div>
      <div class="mb-3">
        <label for="confirm_password" class="form-label">Confirm New Password (leave blank if no change):</label>
        <input type="password" class="form-control" id="confirm_password" name="confirm_password">
      </div>
      <button type="submit" class="btn btn-primary">Update</button>
    </form>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>