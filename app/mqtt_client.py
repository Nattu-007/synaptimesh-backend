# app/mqtt_client.py
# MQTT client — publisher + subscriber with auto-reconnect and structured logging

import json
import uuid
import time
import threading
import paho.mqtt.client as mqtt

from app.config  import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from app.router  import get_topic
from app.logger  import get_logger
from app.exceptions import MQTTConnectionError, MQTTPublishError, MQTTNotConnectedError

logger = get_logger(__name__)

SUBSCRIBE_TOPIC    = "synaptimesh/commands/#"
PUBLISH_TOPIC      = "synaptimesh/commands/desktop"
RECONNECT_DELAY    = 5
MAX_RECONNECT_TRIES = 10

# ── Callbacks ──────────────────────────────────────────────────────────────────

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(SUBSCRIBE_TOPIC)
        logger.info(f"Subscribed to {SUBSCRIBE_TOPIC}")
        client._synaptimesh_connected = True
        client._synaptimesh_reconnect_count = 0
    else:
        logger.error(f"MQTT connection refused — return code {rc}")
        client._synaptimesh_connected = False


def on_disconnect(client, userdata, rc):
    client._synaptimesh_connected = False
    if rc != 0:
        logger.warning(f"Unexpected MQTT disconnect (rc={rc}). Starting auto-reconnect...")
        _auto_reconnect(client)


def on_message(client, userdata, msg):
    """Triggered when a message arrives on any subscribed topic."""
    logger.info(f"Message on topic '{msg.topic}'")
    try:
        payload = json.loads(msg.payload.decode())
        logger.debug(f"Payload: {payload}")

        # Avoid circular imports
        from app.schema     import validate_command
        from app.dispatcher import dispatch_command

        validated, error = validate_command(payload)
        if error:
            logger.warning(f"Validation failed: {error}")
            return

        result = dispatch_command(validated)
        logger.info(f"Dispatch result: {result}")

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON payload: {e}")
    except Exception as e:
        logger.error(f"Error processing MQTT message: {e}", exc_info=True)


# ── Auto-reconnect ─────────────────────────────────────────────────────────────

def _auto_reconnect(client):
    """Background thread — retries connection up to MAX_RECONNECT_TRIES."""
    def _loop():
        count = getattr(client, "_synaptimesh_reconnect_count", 0)
        while not getattr(client, "_synaptimesh_connected", False) and count < MAX_RECONNECT_TRIES:
            count += 1
            client._synaptimesh_reconnect_count = count
            logger.info(f"Reconnect attempt {count}/{MAX_RECONNECT_TRIES}...")
            try:
                client.reconnect()
                time.sleep(0.5)
                if getattr(client, "_synaptimesh_connected", False):
                    logger.info("Reconnected successfully.")
                    return
            except Exception as e:
                logger.warning(f"Reconnect attempt {count} failed: {e}")
            time.sleep(RECONNECT_DELAY)
        if not getattr(client, "_synaptimesh_connected", False):
            logger.error("Max MQTT reconnect attempts reached. Giving up.")

    threading.Thread(target=_loop, daemon=True).start()


# ── Client Setup ───────────────────────────────────────────────────────────────

client = mqtt.Client(client_id="synaptimesh-backend")
client._synaptimesh_connected       = False
client._synaptimesh_reconnect_count = 0
client.on_connect    = on_connect
client.on_disconnect = on_disconnect
client.on_message    = on_message


def connect():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        time.sleep(0.5)
        logger.info(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
    except Exception as e:
        logger.error(f"MQTT connect failed: {e}")
        raise MQTTConnectionError(MQTT_BROKER, MQTT_PORT)


def publish_command(validated: dict):
    if not getattr(client, "_synaptimesh_connected", False):
        raise MQTTNotConnectedError()

    command = validated.get("command")
    topic   = get_topic(command) or PUBLISH_TOPIC

    message = {
        "correlation_id": str(uuid.uuid4())[:8],
        "command":        command,
        "confidence":     validated.get("confidence"),
        "source":         validated.get("source", "EEG"),
        "timestamp":      validated.get("timestamp") or time.time(),
        "target":         topic.split("/")[-1],
    }

    payload = json.dumps(message)
    result  = client.publish(topic, payload, qos=1)

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        logger.info(f"Published → {topic} | cmd={command} | id={message['correlation_id']}")
    else:
        raise MQTTPublishError(topic, f"rc={result.rc}")


def is_connected() -> bool:
    return getattr(client, "_synaptimesh_connected", False)
