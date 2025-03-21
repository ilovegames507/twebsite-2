const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files (optional)
app.use(express.static("public"));

// Basic route
app.get("/", (req, res) => {
  res.send("Hello, Express.js is running!");
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
