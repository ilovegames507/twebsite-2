// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyD1Ys1GB31nGOvNi9SC38n30MORxZzc10s",
  authDomain: "twebsite-94f5b.firebaseapp.com",
  databaseURL: "https://twebsite-94f5b-default-rtdb.firebaseio.com",
  projectId: "twebsite-94f5b",
  storageBucket: "twebsite-94f5b.appspot.com",  // Fixed storage bucket
  messagingSenderId: "585359123086",
  appId: "1:585359123086:web:6a6dd51e6781063a455fdf",
  measurementId: "G-YPBH30GZVB"
};

// Your Firebase configuration
// Removed redundant declaration of firebaseConfig


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
