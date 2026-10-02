<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Dashboard</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <a class="nav-link" href="logout.php">Logout</a>
        </li>
      </ul>
    </div>
  </nav>

  <div class="container mt-4">
    <h1 class="text-center mb-4">Welcome, <?php echo $_SESSION['user_name'];?>!</h1>
    <h2 class="mb-3">Users</h2>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Username</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <?php
        require_once 'functions.php';
        $result = getAllUsers();

        if ($result) {
          foreach ($result as $user) {
            echo "<tr>";
            echo "<td>". $user['id']. "</td>";
            echo "<td>". $user['name']. "</td>";
            echo "<td>". $user['email']. "</td>";
            echo "<td>". $user['username']. "</td>";
            echo "<td>
                    <a href='update_user.php?id=". $user['id']. "' class='btn btn-primary'>Edit</a>
                    <a href='delete_user.php?id=". $user['id']. "' class='btn btn-danger' onclick='return confirm(\"Are you sure you want to delete this user?\")'>Delete</a>
                  </td>";
            echo "</tr>";
          }
        } else {
          echo "<tr><td colspan='5'>No users found</td></tr>";
        }
       ?>
      </tbody>
    </table>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>