// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const newLocal = {
    "apiKey": "AIzaSyD1Ys1GB31nGOvNi9SC38n30MORxZzc10s",
    "authDomain": "your-project.firebaseapp.com",
    "databaseURL": "https://your-project-default-rtdb.firebaseio.com/",
    "storageBucket": "your-project.appspot.com",
    "messagingSenderId": "your-messaging-id",
    "appId": "your-app-id",
};
// Your Firebase configuration
const firebaseConfig = newLocal


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Google Login Function
document.getElementById("googleLoginBtn").addEventListener("click", () => {
  signInWithPopup(auth, provider)
    .then((result) => {
      const user = result.user;
      console.log("Logged in as:", user.displayName);
      document.getElementById("logoutBtn").style.display = "block";
      document.getElementById("googleLoginBtn").style.display = "none";
    })
    .catch((error) => console.error("Login failed:", error.message));
});

// Logout Function
document.getElementById("logoutBtn").addEventListener("click", () => {
  signOut(auth)
    .then(() => {
      console.log("User signed out");
      document.getElementById("logoutBtn").style.display = "none";
      document.getElementById("googleLoginBtn").style.display = "block";
    })
    .catch((error) => console.error("Logout failed:", error.message));
});

// Monitor Authentication State
onAuthStateChanged(auth, (user) => {
  if (user) {
    console.log("User is signed in:", user.displayName);
    document.getElementById("logoutBtn").style.display = "block";
    document.getElementById("googleLoginBtn").style.display = "none";
  } else {
    console.log("No user signed in");
    document.getElementById("logoutBtn").style.display = "none";
    document.getElementById("googleLoginBtn").style.display = "block";
  }
});
