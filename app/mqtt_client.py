# app/mqtt_client.py
import paho.mqtt.client as mqtt
import json
from app.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

client = mqtt.Client(client_id="synaptimesh-backend")

def on_connect(c, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected to broker at {MQTT_BROKER}:{MQTT_PORT}")
    else:
        print(f"[MQTT] Connection failed — code {rc}")

def on_disconnect(c, userdata, rc):
    print(f"[MQTT] Disconnected — code {rc}. Reconnecting...")
    try:
        c.reconnect()
    except Exception as e:
        print(f"[MQTT] Reconnect failed: {e}")

client.on_connect    = on_connect
client.on_disconnect = on_disconnect

def connect():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
    except Exception as e:
        print(f"[MQTT] Could not connect: {e}")

def publish_command(validated: dict):
    payload = json.dumps(validated)
    result  = client.publish(MQTT_TOPIC, payload)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"[MQTT] Published → {MQTT_TOPIC}: {payload}")
    else:
        print(f"[MQTT] Publish failed — rc={result.rc}")

# Connect on import
connect()