<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
require_once __DIR__ . '/db_connect.php';

function registerUser($name, $email, $username, $password)
{
    global $conn;
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);
    $stmt = $conn->prepare("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)");
    if (!$stmt) return false;
    $stmt->bind_param("ssss", $name, $email, $username, $hashed_password);
    return $stmt->execute();
}

function loginUser($username, $password)
{
    global $conn;
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ? OR email = ?");
    if (!$stmt) return false;
    $stmt->bind_param("ss", $username, $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result && $result->num_rows === 1) {
        $user = $result->fetch_assoc();
        if (password_verify($password, $user['password'])) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['user_name'] = $user['name'];
            $_SESSION['username'] = $user['username'];
            return true;
        }
    }
    return false;
}

function getAllUsers()
{
    global $conn;
    $stmt = $conn->prepare("SELECT id, name, email, username, created_at FROM users ORDER BY id DESC");
    if (!$stmt) return [];
    $stmt->execute();
    $result = $stmt->get_result();
    return $result ? $result->fetch_all(MYSQLI_ASSOC) : [];
}

function deleteUser($id)
{
    global $conn;
    $stmt = $conn->prepare("DELETE FROM users WHERE id = ?");
    if (!$stmt) return false;
    $stmt->bind_param("i", $id);
    return $stmt->execute();
}

function updateUser($id, $name, $email, $username, $password = null)
{
    global $conn;
    if (!empty($password)) {
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        $stmt = $conn->prepare("UPDATE users SET name=?, email=?, username=?, password=? WHERE id=?");
        if (!$stmt) return false;
        $stmt->bind_param("ssssi", $name, $email, $username, $hashed_password, $id);
    } else {
        $stmt = $conn->prepare("UPDATE users SET name=?, email=?, username=? WHERE id=?");
        if (!$stmt) return false;
        $stmt->bind_param("sssi", $name, $email, $username, $id);
    }
    return $stmt->execute();
}
?>