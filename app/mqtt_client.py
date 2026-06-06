# app/mqtt_client.py
import paho.mqtt.client as mqtt
import json
import uuid
import time
from app.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from app.router import get_topic

# ─── Topics ─────────────────────────────────────────────────────────────────
SUBSCRIBE_TOPIC  = "synaptimesh/commands/#"    # Listen to ALL command topics
PUBLISH_TOPIC    = "synaptimesh/commands/desktop"

# ─── Callbacks ──────────────────────────────────────────────────────────────

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected to broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(SUBSCRIBE_TOPIC)
        print(f"[MQTT] Subscribed to {SUBSCRIBE_TOPIC}")
    else:
        print(f"[MQTT] Connection failed — code {rc}")

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected — code {rc}. Reconnecting...")
    try:
        client.reconnect()
    except Exception as e:
        print(f"[MQTT] Reconnect failed: {e}")

def on_message(client, userdata, msg):
    """
    Triggered when a message arrives on any subscribed topic.
    Parses the payload and dispatches the command.
    """
    print(f"\n[MQTT] Message received on topic: {msg.topic}")

    try:
        payload = json.loads(msg.payload.decode())
        print(f"[MQTT] Payload: {payload}")

        # Import here to avoid circular imports
        from app.schema import validate_command
        from app.dispatcher import dispatch_command

        # Validate
        validated, error = validate_command(payload)
        if error:
            print(f"[MQTT] Validation failed: {error}")
            return

        # Dispatch → executes on PC
        result = dispatch_command(validated)
        print(f"[MQTT] Dispatch result: {result}")

    except json.JSONDecodeError as e:
        print(f"[MQTT] Invalid JSON: {e}")
    except Exception as e:
        print(f"[MQTT] Error processing message: {e}")

# ─── Client Setup ────────────────────────────────────────────────────────────

client = mqtt.Client(client_id="synaptimesh-backend")
client.on_connect    = on_connect
client.on_disconnect = on_disconnect
client.on_message    = on_message

def connect():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        print(f"[MQTT] Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
    except Exception as e:
        print(f"[MQTT] Could not connect: {e}")

def publish_command(validated: dict):
    command = validated.get("command")
    topic   = get_topic(command) or PUBLISH_TOPIC

    message = {
        "correlation_id": str(uuid.uuid4())[:8],
        "command":        command,
        "confidence":     validated.get("confidence"),
        "source":         validated.get("source", "EEG"),
        "timestamp":      validated.get("timestamp") or time.time(),
        "target":         topic.split("/")[-1]
    }

    payload = json.dumps(message)
    result  = client.publish(topic, payload)

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"[MQTT] Published → {topic}: {payload}")
    else:
        print(f"[MQTT] Publish failed — rc={result.rc}")

connect()