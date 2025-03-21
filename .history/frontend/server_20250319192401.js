const express = require("express");
const cors = require("cors");
const path = require("path");
const admin = require("firebase-admin");

const serviceAccount = require("./serviceAccountKey.json");


admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
});

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public"))); // Serve static files

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

// Firebase Authentication API (Backend Authentication)
app.post("/google-login", async (req, res) => {
    try {
        const { token } = req.body;
        const decodedToken = await admin.auth().verifyIdToken(token);
        return res.json({ message: "User authenticated", uid: decodedToken.uid, email: decodedToken.email });
    } catch (error) {
        return res.status(401).json({ error: error.message });
    }
});

// Start Server
app.listen(PORT, () => {
    console.log(`🚀 Server running at http://localhost:${PORT}`);
});
