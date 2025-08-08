// Toggle password visibility
function togglePassword(id) {
  const input = document.getElementById(id);
  if (!input) return;
  const type = input.type === 'password' ? 'text' : 'password';
  input.type = type;
}



// Show login error message
function showLoginError(message) {
  const errorDiv = document.getElementById('login-error');
  errorDiv.textContent = message;
  errorDiv.classList.remove('hidden');
}

// Hide login error message
function hideLoginError() {
  const errorDiv = document.getElementById('login-error');
  errorDiv.classList.add('hidden');
}

// Handle login logic (replace with real backend validation)
function handleLogin() {
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;

  // Dummy validation — replace with actual server-side check
  if (username === 'admin' && password === '1234') {
    alert('Login successful!');
    hideLoginError();
    // Redirect or proceed to dashboard
  } else {
    showLoginError('Invalid username or password.');
  }
}

// Switch between login and signup forms
function showSignup() {
  document.getElementById('login-form').classList.add('hidden');
  document.getElementById('signup-form').classList.remove('hidden');
  hideLoginError();
}

function showLogin() {
  document.getElementById('signup-form').classList.add('hidden');
  document.getElementById('login-form').classList.remove('hidden');
  hideLoginError();
}


// Clear error when user types again
document.addEventListener('DOMContentLoaded', () => {
  const loginPasswordInput = document.getElementById('login-password');
  if (loginPasswordInput) {
    loginPasswordInput.addEventListener('input', hideLoginError);
  }
});
