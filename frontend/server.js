const express = require("express");
const cors = require("cors");
const path = require("path");
const admin = require("firebase-admin");
const axios = require("axios");

const serviceAccount = require("./serviceAccountKey.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore();
const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// ✅ Serve Static Pages
app.get("/", (req, res) => res.sendFile(path.join(__dirname, "public", "index.html")));
app.get("/services", (req, res) => res.sendFile(path.join(__dirname, "public", "service.html")));
app.get("/about", (req, res) => res.sendFile(path.join(__dirname, "public", "about.html")));
app.get("/contact", (req, res) => res.sendFile(path.join(__dirname, "public", "contact.html")));
app.get("/login", (req, res) => res.sendFile(path.join(__dirname, "public", "login&signup.html")));
app.get("/vip", (req, res) => res.sendFile(path.join(__dirname, "public", "vip.html")));
app.get("/dashboard", (req, res) => res.sendFile(path.join(__dirname, "public", "dashboard.html")));
app.get("/legal", (req, res) => res.sendFile(path.join(__dirname, "public", "legal.html")));

// ✅ Google Login
app.post("/google-login", async (req, res) => {
    try {
        const { token } = req.body;
        const decodedToken = await admin.auth().verifyIdToken(token);
        return res.json({ message: "User authenticated", uid: decodedToken.uid, email: decodedToken.email });
    } catch (error) {
        console.error("Google Login Error:", error);
        return res.status(401).json({ error: error.message });
    }
});

// ✅ Calendly Webhook Endpoint
app.post("/webhook", async (req, res) => {
    try {
        const data = req.body;
        console.log("📩 Received Webhook:", JSON.stringify(data, null, 2));

        const eventType = data.event;
        if (eventType === "invitee.created") {
            const invitee = data.payload.invitee;
            const event = data.payload.event;

            const appointmentData = {
                name: invitee.name,
                email: invitee.email,
                event_time: event.start_time,
                questions_and_answers: invitee.questions_and_answers || [],
                status: "booked"
            };

            // ✅ Save to Firestore (Ensures doc exists before updating)
            await db.collection("appointments").doc(invitee.email).set(appointmentData, { merge: true });
            return res.status(200).json({ message: "Appointment booked and saved!" });

        } else if (eventType === "invitee.canceled") {
            const email = data.payload.invitee.email;
            await db.collection("appointments").doc(email).set({ status: "canceled" }, { merge: true });
            return res.status(200).json({ message: "Appointment canceled" });
        }

        return res.status(400).json({ message: "Event type not handled" });
    } catch (error) {
        console.error("Webhook Error:", error);
        return res.status(500).json({ error: error.message });
    }
});

// ✅ Register Webhook with Calendly
app.post("/register-webhook", async (req, res) => {
    try {
        const CALENDLY_API_TOKEN = "your_calendly_api_key";  // 🔹 Replace with your actual API key
        const WEBHOOK_URL = "https://yourdomain.com/webhook"; // 🔹 Your webhook endpoint
        const ORG_ID = "your_org_id";  // 🔹 Replace with your Calendly org ID

        const response = await axios.post(
            "https://api.calendly.com/webhook_subscriptions",
            {
                url: WEBHOOK_URL,
                events: ["invitee.created", "invitee.canceled"],
                organization: `https://api.calendly.com/organizations/${ORG_ID}`
            },
            {
                headers: {
                    Authorization: `Bearer ${CALENDLY_API_TOKEN}`,
                    "Content-Type": "application/json"
                },
            }
        );

        res.json(response.data);
    } catch (error) {
        console.error("Calendly Webhook Registration Error:", error.response ? error.response.data : error.message);
        res.status(500).json({ error: "Failed to register webhook" });
    }
});
// ✅ Handle contact form submission
app.post("/contact", async (req, res) => {
    try {
        const { name, email, phone, message } = req.body;

        if (!name || !email || !message) {
            return res.status(400).json({ error: "Missing required fields" });
        }

        const contactData = {
            name,
            email,
            phone: phone || null,
            message,
            submitted_at: new Date().toISOString()
        };

        await db.collection("contact_submissions").add(contactData);

        res.status(200).json({ message: "Message received! We'll get back to you soon." });
    } catch (error) {
        console.error("Contact Form Error:", error);
        res.status(500).json({ error: "Something went wrong. Try again later." });
    }
});


// ✅ Start Server
app.listen(PORT, () => {
    console.log(`🚀 Server running at http://localhost:${PORT}`);
});
