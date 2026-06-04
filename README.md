# SynaptiMesh Backend

## Overview

SynaptiMesh Backend is a Flask-based REST API service that receives validated Brain-Computer Interface (BCI) commands and publishes them to an MQTT broker for downstream processing. The service acts as the communication layer between EEG signal processing modules and connected applications or devices.

---

## Features

* REST API endpoint for receiving commands
* Pydantic-based payload validation
* MQTT message publishing
* Environment-based configuration
* Error handling and validation responses
* Lightweight Flask server architecture

---

## Project Structure

```text
synaptimesh-backend/
│
├── app/
│   ├── __init__.py
│   ├── server.py
│   ├── schema.py
│   └── mqtt_client.py
│
├── logs/
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## System Architecture

```text
Client Application
        │
        ▼
 REST API (Flask)
        │
        ▼
 Payload Validation
     (Pydantic)
        │
        ▼
 MQTT Publisher
        │
        ▼
 MQTT Broker
   (Mosquitto)
        │
        ▼
 Connected Devices /
 Downstream Services
```

---

## Requirements

* Python 3.10+
* Mosquitto MQTT Broker
* Git
* Virtual Environment

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd synaptimesh-backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root.

```env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC_PREFIX=synaptimesh

FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
```

---

## Running the MQTT Broker

Start Mosquitto:

```powershell
mosquitto -v
```

Verify broker availability:

```powershell
netstat -ano | findstr :1883
```

---

## Running the Backend Server

```bash
python -m app.server
```

Expected output:

```text
[MQTT] Connected to broker at localhost:1883
 * Running on http://127.0.0.1:5000
```

---

## API Endpoints

### Health Check

#### Request

```http
GET /
```

#### Response

```json
{
  "service": "SynaptiMesh Backend",
  "status": "running"
}
```

---

### Receive Command

#### Request

```http
POST /receive-command
Content-Type: application/json
```

#### Example Payload

```json
{
  "command": "PLAY",
  "confidence": 0.95
}
```

#### Successful Response

```json
{
  "status": "ok",
  "command": {
    "command": "PLAY",
    "confidence": 0.95,
    "timestamp": null,
    "source": "EEG"
  }
}
```

#### Error Response

```json
{
  "error": "Invalid or missing JSON payload"
}
```

---

## Payload Schema

| Field      | Type   | Required | Description            |
| ---------- | ------ | -------- | ---------------------- |
| command    | string | Yes      | BCI command            |
| confidence | float  | Yes      | Model confidence score |
| timestamp  | float  | No       | Command timestamp      |
| source     | string | No       | Signal source          |

---

## Testing

### Valid Request

```powershell
$body = @{
    command = "PLAY"
    confidence = 0.95
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/receive-command" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Invalid Request

```powershell
$body = @{
    bad_field = "xyz"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/receive-command" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Expected Result:

```text
HTTP 400 Bad Request
```

---

## MQTT Integration

Commands are published to the configured MQTT topic for downstream consumers.

Example MQTT Message:

```json
{
  "command": "PLAY",
  "confidence": 0.95
}
```

---

## Future Enhancements

* JWT Authentication
* HTTPS Support
* Docker Deployment
* Command Persistence
* Real-Time Dashboard
* EEG Stream Integration
* WebSocket Support
* Automated Unit Testing

---

## Author

SynaptiMesh Python Backend Team

---

## License

Internal Research and Development Project.
