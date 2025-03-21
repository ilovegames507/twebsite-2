const { onRequest } = require("firebase-functions/v2/https");
const express = require("express");
const cors = require("cors");
const admin = require("firebase-admin");
const path = require("path");

admin.initializeApp();

const app = express();
app.use(cors());
app.use(express.json());

// Serve static files (Firebase Hosting serves front-end)
app.use(express.static(path.join(__dirname, "../public")));

// Routes
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "../public/index.html"));
});

app.post("/api/google-login", async (req, res) => {
    try {
        const { token } = req.body;
        const decodedToken = await admin.auth().verifyIdToken(token);
        return res.json({ message: "User authenticated", uid: decodedToken.uid, email: decodedToken.email });
    } catch (error) {
        return res.status(401).json({ error: error.message });
    }
});

// Export Express app as a Firebase Function
exports.app = onRequest(app);
