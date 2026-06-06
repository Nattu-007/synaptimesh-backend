# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

MQTT_BROKER          = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT            = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC           = os.getenv("MQTT_TOPIC", "synaptimesh/commands")
SERVER_HOST          = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT          = int(os.getenv("SERVER_PORT", 5000))
SERVER_DEBUG         = os.getenv("SERVER_DEBUG", "True") == "True"
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.70))

# ── Chatbot — Groq (free tier) ────────────────────────────────────────────────
# Get your free API key at: https://console.groq.com  (no credit card required)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Model options (all free tier):
#   "llama-3.3-70b-versatile"  — best quality, GPT-4o level  ← default
#   "llama3-8b-8192"           — fastest, lowest latency
#   "mixtral-8x7b-32768"       — long context (32K tokens)
#   "gemma2-9b-it"             — Google's Gemma, efficient
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
