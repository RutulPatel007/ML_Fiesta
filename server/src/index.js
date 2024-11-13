import express from "express";
import { PrismaClient } from "@prisma/client";
import axios from "axios";
import crypto from "crypto";

const app = express();
const prisma = new PrismaClient();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Generate a unique token
const generateToken = () => crypto.randomBytes(20).toString("hex");

// Route 1: Provide One-Time Token or Verify Existing Token
app.post("/token", async (req, res) => {
  const { token } = req.body;

  try {
    if (token) {
      // Check if the provided token exists in the database
      const user = await prisma.user.findUnique({ where: { token } });
      if (user) {
        return res.status(200).json({ token: user.token, message: "Token is valid." });
      }
      return res.status(404).json({ error: "Token not found." });
    } else {
      // No token provided, so create a new user with a unique token
      const newToken = generateToken();
      const newUser = await prisma.user.create({
        data: { token: newToken },
      });
      return res.status(201).json({ token: newUser.token });
    }
  } catch (error) {
    console.error("Error in /token route:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Route 2: Retrieve Chat History
app.get("/history", async (req, res) => {
  const { token } = req.query;

  if (!token) return res.status(400).json({ error: "Token required." });

  try {
    const user = await prisma.user.findUnique({ where: { token } });
    if (!user) return res.status(404).json({ error: "User not found." });

    const history = await prisma.chatMessage.findMany({
      where: { userId: user.id },
      orderBy: { createdAt: "asc" },
    });

    res.status(200).json({ history });
  } catch (error) {
    console.error("Error retrieving history:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Route 3: Add New Message & Get AI Response
app.post("/chat", async (req, res) => {
  const { token, message } = req.body;

  if (!token || !message) return res.status(400).json({ error: "Token and message are required." });

  try {
    const user = await prisma.user.findUnique({ where: { token } });
    if (!user) return res.status(404).json({ error: "User not found." });

    // Store user's message in the database with type 'USER'
    await prisma.chatMessage.create({
      data: {
        userId: user.id,
        content: message,
        type: "USER",
      },
    });

    // Mock AI Assistant API call for response
    const aiResponse = await axios.post("https://e39e-35-197-1-120.ngrok-free.app/generate", { input:message });


    console.log(aiResponse);


    // Store AI assistant's response in the database with type 'ASSISTANT'
    const assistantMessage = await prisma.chatMessage.create({
      data: {
        userId: user.id,
        content: aiResponse.data.output,
        type: "ASSISTANT",
      },
    });

    res.status(201).json({ userMessage: message, assistantResponse: assistantMessage });
  } catch (error) {
    console.error("Error processing chat message:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
