$(document).ready(function () {
	var loginModal = document.getElementById("loginContainer");
	var signupModal = document.getElementById("signupContainer");

	// Get the button that opens the modal
	var loginBtn = document.getElementById("loginButton");
	var signupBtn = document.getElementById("signupButton");

	// Get the <span> element that closes the modal
	var signupClose = document.getElementById("signupClose");
	var loginClose = document.getElementById("loginClose");

	var showSignup = document.getElementById("showSignup");
	var showLogin = document.getElementById("showLogin");

	// When the user clicks on the button, open the modal
	loginBtn.onclick = function () {
		loginModal.style.display = "block";
	}
	signupBtn.onclick = function () {
		signupModal.style.display = "block";
	}

	showSignup.onclick = function () {
		loginModal.style.display = "none";
		signupModal.style.display = "block";
	}

	showLogin.onclick = function () {
		signupModal.style.display = "none";
		loginModal.style.display = "block";

	}

	// When the user clicks on <span> (x), close the modal
	signupClose.onclick = function () {
		signupModal.style.display = "none";
	}
	loginClose.onclick = function () {
		loginModal.style.display = "none";
	}
});