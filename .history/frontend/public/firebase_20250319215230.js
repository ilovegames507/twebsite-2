// Import Firebase SDKs
import { initializeApp } from "firebase/app";
import { 
  getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged 
} from "firebase/auth";
import { getFirestore } from "firebase/firestore"; // Firestore Import

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD1Ys1GB31nGOvNi9SC38n30MORxZzc10s",
  authDomain: "twebsite-94f5b.firebaseapp.com",
  databaseURL: "https://twebsite-94f5b-default-rtdb.firebaseio.com",
  projectId: "twebsite-94f5b",
  storageBucket: "twebsite-94f5b.appspot.com", // ✅ FIXED
  messagingSenderId: "585359123086",
  appId: "1:585359123086:web:46aff2d7761cfc4d455fdf",
  measurementId: "G-RGVD6G7JYD"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app); // Initialize Firestore
const provider = new GoogleAuthProvider();

// Google Login
document.getElementById("googleLoginBtn").addEventListener("click", () => {
  signInWithPopup(auth, provider)
    .then((result) => {
      console.log("Logged in as:", result.user.displayName);
      document.getElementById("logoutBtn").style.display = "block";
      document.getElementById("googleLoginBtn").style.display = "none";
    })
    .catch((error) => console.error("Login failed:", error.message));
});

// Handle Auth State Persistence ✅
onAuthStateChanged(auth, (user) => {
  if (user) {
    console.log("User is signed in:", user.displayName);
    document.getElementById("logoutBtn").style.display = "block";
    document.getElementById("googleLoginBtn").style.display = "none";
  } else {
    console.log("No user signed in.");
    document.getElementById("logoutBtn").style.display = "none";
    document.getElementById("googleLoginBtn").style.display = "block";
  }
});

// Logout
document.getElementById("logoutBtn").addEventListener("click", () => {
  signOut(auth)
    .then(() => {
      console.log("User signed out");
    })
    .catch((error) => console.error("Logout failed:", error.message));
});
