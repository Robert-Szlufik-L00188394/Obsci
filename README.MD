Observability Pipeline for SNMP-enabled IoT Devices

📦 Overview

This project provides a lightweight, containerised observability pipeline designed for data scientists and engineers working with SNMP-enabled IoT devices (e.g., PDUs, environmental sensors). The pipeline is built using Docker, Docker Compose, Telegraf, InfluxDB, and Grafana. It features structured logging, automated configuration, and operates in two modes: synthetic (for testing) and SNMP (for real devices).

🚀 Features

🔧 Modular, containerised architecture

🐍 Python-based launcher and teardown scripts

📊 Real-time data visualisation with Grafana

🗃️ Time-series data storage in InfluxDB

🧪 Synthetic mode for demo and debugging

📡 SNMP polling for real devices

🪵 Structured logging with daily rotation

🔁 Git-friendly device configuration using JSON

📁 Directory Structure

.
├── launch_pipeline.py         # Launch script
├── stop_pipeline.py           # Teardown script
├── devices.json               # SNMP device configuration
├── http-server/              # Synthetic data source
├── grafana/
│   └── provisioning/         # Preloaded dashboard JSON
├── telegraf/
│   └── templates/            # Base config template
├── logs/                     # Daily logs
└── README.md                 # You're here!

⚙️ Requirements

Docker

Docker Compose

Python 3.7+

🛠️ Usage

1. Clone the Repository

git clone https://github.com/your-org/observability-pipeline.git
cd observability-pipeline

2. Run in Synthetic Mode

python launch_pipeline.py --synthetic

3. Run in SNMP Mode

Edit devices.json with your SNMP device details:

[
  {
    "id": "pdu-1",
    "ip": "fd00::1",
    "version": "2c",
    "community": "public"
  }
]

Then launch:

python launch_pipeline.py --devices

4. Stop the Pipeline

python stop_pipeline.py

📊 Grafana Dashboard

Access the Grafana UI at:

http://localhost:3000

Default login:

Username: admin

Password: admin

Preloaded dashboards will appear automatically. You can modify or clone them via the Grafana UI.

📝 Logging

Log files are stored in the logs/ directory with filenames like:

logs/05-07-2025-obsci.log

These contain:

Launch parameters

Docker image versions

SNMP device summary

Telegraf logs

🧩 Extensibility

Future enhancements can include:

MQTT and Modbus protocol support

Container health checks and alerts

Remote Grafana access with user authentication

Log streaming to external monitoring stacks

🧪 Testing & Stability

The pipeline is designed to run on modest systems (e.g., 2 vCPU, 4 GB RAM) and tested for fast startup (~10s), with full readiness in ~30s.

📄 License

MIT License

Built to bridge the gap between DevOps and Data Science.

