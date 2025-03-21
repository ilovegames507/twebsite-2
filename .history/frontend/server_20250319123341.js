const express = require("express");
const cors = require("cors");
const path = require("path");
const admin = require("firebase-admin");
const firebase = require("firebase/app");
require("firebase/auth");

// Firebase Config
const firebaseConfig = {
    apiKey: "AIzaSyD1Ys1GB31nGOvNi9SC38n30MORxZzc10s",
    authDomain: "your-project.firebaseapp.com",
    projectId: "twebsite-94f5b",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "585359123086",
    appId: "your-app-id",
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Initialize Firebase Admin (for verifying tokens)
const serviceAccount = require("./path/to/your/serviceAccountKey.json");
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
});

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public"))); // Serve static files (HTML, CSS, JS)

// Routes for static HTML pages
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/services", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "login&signup.html"));
});

app.get("/about", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "about.html"));
});

app.get("/contact", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "contact.html"));
});

app.get("/login", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "login&signup.html"));
});

// Firebase Authentication API
app.post("/google-login", async (req, res) => {
    try {
        const { token } = req.body;
        const decodedToken = await admin.auth().verifyIdToken(token);
        return res.json({ message: "User authenticated", uid: decodedToken.uid, email: decodedToken.email });
    } catch (error) {
        return res.status(401).json({ error: error.message });
    }
});

app.post("/signup", async (req, res) => {
    try {
        const { email, password } = req.body;
        const userCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
        return res.json({ message: "User created successfully", uid: userCredential.user.uid });
    } catch (error) {
        return res.status(400).json({ error: error.message });
    }
});

app.post("/login", async (req, res) => {
    try {
        const { email, password } = req.body;
        const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
        return res.json({ message: "Login successful", uid: userCredential.user.uid });
    } catch (error) {
        return res.status(400).json({ error: error.message });
    }
});

// Start Server
app.listen(PORT, () => {
    console.log(`🚀 Server running at http://localhost:${PORT}`);
});
