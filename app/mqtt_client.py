# app/mqtt_client.py
# SynaptiMesh MQTT Client
# Publisher + Subscriber + Auto Reconnect + WebApp Support

import json
import uuid
import time
import threading

import paho.mqtt.client as mqtt

from app.config import (
    MQTT_BROKER,
    MQTT_PORT
)

from app.router import get_topic

from app.logger import get_logger

from app.exceptions import (
    MQTTConnectionError,
    MQTTPublishError,
    MQTTNotConnectedError
)

logger = get_logger(__name__)

SUBSCRIBE_TOPIC = "synaptimesh/commands/#"

DEFAULT_TOPIC = "synaptimesh/commands/desktop"

STATUS_TOPIC = "synaptimesh/status"

RECONNECT_DELAY = 5

MAX_RECONNECT_TRIES = 10


# =====================================================
# MQTT CALLBACKS
# =====================================================

def on_connect(
    client,
    userdata,
    flags,
    rc
):

    if rc == 0:

        client._synaptimesh_connected = True

        client._synaptimesh_reconnect_count = 0

        logger.info(
            f"Connected to MQTT Broker "
            f"{MQTT_BROKER}:{MQTT_PORT}"
        )

        client.subscribe(
            SUBSCRIBE_TOPIC
        )

        logger.info(
            f"Subscribed -> "
            f"{SUBSCRIBE_TOPIC}"
        )

    else:

        client._synaptimesh_connected = False

        logger.error(
            f"MQTT Connection Failed "
            f"(rc={rc})"
        )


def on_disconnect(
    client,
    userdata,
    rc
):

    client._synaptimesh_connected = False

    if rc != 0:

        logger.warning(
            "Unexpected disconnect"
        )

        _auto_reconnect(client)


def on_publish(
    client,
    userdata,
    mid
):

    logger.debug(
        f"Publish ACK received "
        f"(mid={mid})"
    )


def on_message(
    client,
    userdata,
    msg
):

    logger.info(
        f"MQTT Message -> "
        f"{msg.topic}"
    )

    try:

        payload = json.loads(
            msg.payload.decode()
        )

        logger.debug(
            f"Payload={payload}"
        )

        from app.schema import (
            validate_command
        )

        from app.dispatcher import (
            dispatch_command
        )

        validated, error = (
            validate_command(
                payload
            )
        )

        if error:

            logger.warning(
                f"Validation failed "
                f"{error}"
            )

            return

        result = dispatch_command(
            validated
        )

        logger.info(
            f"Dispatch Result "
            f"{result}"
        )

    except json.JSONDecodeError as e:

        logger.error(
            f"JSON Decode Error "
            f"{e}"
        )

    except Exception as e:

        logger.error(
            f"MQTT Processing Error "
            f"{e}",
            exc_info=True
        )


# =====================================================
# RECONNECT
# =====================================================

def _auto_reconnect(client):

    def reconnect_loop():

        count = getattr(
            client,
            "_synaptimesh_reconnect_count",
            0
        )

        while (
            not getattr(
                client,
                "_synaptimesh_connected",
                False
            )
            and count < MAX_RECONNECT_TRIES
        ):

            count += 1

            client._synaptimesh_reconnect_count = (
                count
            )

            logger.info(
                f"Reconnect "
                f"{count}/"
                f"{MAX_RECONNECT_TRIES}"
            )

            try:

                client.reconnect()

                time.sleep(1)

                if getattr(
                    client,
                    "_synaptimesh_connected",
                    False
                ):

                    logger.info(
                        "MQTT Reconnected"
                    )

                    return

            except Exception as e:

                logger.warning(
                    f"Reconnect failed "
                    f"{e}"
                )

            time.sleep(
                RECONNECT_DELAY
            )

        logger.error(
            "Max reconnect attempts reached"
        )

    threading.Thread(
        target=reconnect_loop,
        daemon=True
    ).start()


# =====================================================
# CLIENT SETUP
# =====================================================

client = mqtt.Client(
    client_id="synaptimesh-backend"
)

client._synaptimesh_connected = False

client._synaptimesh_reconnect_count = 0

client.on_connect = on_connect

client.on_disconnect = on_disconnect

client.on_publish = on_publish

client.on_message = on_message


# =====================================================
# CONNECTION
# =====================================================

def connect():

    try:

        logger.info(
            f"Connecting MQTT "
            f"{MQTT_BROKER}:{MQTT_PORT}"
        )

        client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            keepalive=60
        )

        client.loop_start()

        time.sleep(0.5)

    except Exception as e:

        logger.error(
            f"MQTT Connect Failed "
            f"{e}"
        )

        raise MQTTConnectionError(
            MQTT_BROKER,
            MQTT_PORT
        )


# =====================================================
# PUBLISH
# =====================================================

def publish_command(
    validated: dict
):

    if not getattr(
        client,
        "_synaptimesh_connected",
        False
    ):

        raise MQTTNotConnectedError()

    command = validated.get(
        "command"
    )

    topic = (
        get_topic(command)
        or DEFAULT_TOPIC
    )

    message = {

        "correlation_id":
        str(uuid.uuid4())[:8],

        "command":
        command,

        "confidence":
        validated.get(
            "confidence"
        ),

        "source":
        validated.get(
            "source",
            "EEG"
        ),

        "timestamp":
        validated.get(
            "timestamp"
        )
        or time.time(),

        "target":
        topic.split("/")[-1]
    }

    if "query" in validated:

        message["query"] = (
            validated["query"]
        )

    payload = json.dumps(
        message
    )

    result = client.publish(
        topic,
        payload,
        qos=1
    )

    if (
        result.rc
        == mqtt.MQTT_ERR_SUCCESS
    ):

        logger.info(
            f"Published -> "
            f"{topic} | "
            f"{command} | "
            f"id="
            f"{message['correlation_id']}"
        )

    else:

        raise MQTTPublishError(
            topic,
            f"rc={result.rc}"
        )

    return message


# =====================================================
# STATUS
# =====================================================

def is_connected():

    return getattr(
        client,
        "_synaptimesh_connected",
        False
    )


def connection_status():

    return {

        "connected":
        is_connected(),

        "broker":
        MQTT_BROKER,

        "port":
        MQTT_PORT,

        "reconnect_attempts":
        getattr(
            client,
            "_synaptimesh_reconnect_count",
            0
        )
    }


# =====================================================
# HEALTH CHECK
# =====================================================

def mqtt_health():

    return {

        "service": "mqtt",

        "status":
        "healthy"
        if is_connected()
        else "disconnected",

        "broker":
        MQTT_BROKER,

        "port":
        MQTT_PORT
    }