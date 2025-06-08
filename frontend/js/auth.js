const authLinks = document.getElementById('auth-links');
if (localStorage.getItem('token')) {
  authLinks.innerHTML = '<a href="#" onclick="logout()" class="login">Logout</a>';
} else {
  authLinks.innerHTML = '<a href="login.html" class="login">Login</a> | <a href="register.html" class="register">Register</a>';
}

function logout() {
  localStorage.removeItem('token');
  location.reload();
}
