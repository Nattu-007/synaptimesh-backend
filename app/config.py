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