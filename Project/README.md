# Network Security: Traffic Sniffing and Analysis

A controlled, Docker-based laboratory environment designed for demonstrating network traffic generation, packet sniffing, and analyzing vulnerabilities in clear-text protocols like HTTP and Telnet. This project is created for educational and academic purposes in the field of Computer Security.

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Traffic Generation](#traffic-generation)
  - [Packet Sniffing](#packet-sniffing)
- [Project Structure](#project-structure)
- [Disclaimer](#disclaimer)

## 📖 Overview
This project provides an isolated environment using Docker Compose to simulate a local network with different actors:
* An **Attacker** node configured with sniffing capabilities.
* A **Victim** node simulating a regular user.
* **Vulnerable Servers**, including HTTP and Telnet, allowing you to intercept and analyze unencrypted traffic.

## 🏗️ Architecture
The lab provisions the following containers on a bridged Docker network:
* **Attacker**: Runs Python with tools like Scapy for passive sniffing (`sniffer.py`).
* **Victim**: Designed to initiate connections with the servers using the `generate_traffic.py` script.
* **HTTP Server**: A basic unencrypted web server (`http_server.py`).
* **Telnet Server**: A classic clear-text protocol simulator.

## ⚙️ Prerequisites
To run this project, you will need:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## 🚀 Quick Start
Clone the project repository and bring up the Docker environment in the background:

```bash
# Build and start all containers
docker-compose up --build -d

# Verify containers are running
docker-compose ps
```

## 🛠️ Usage

### 1. Packet Sniffing (Attacker)
Access the attacker container to monitor the network interface and capture packets.

```bash
# Exec into the attacker container
docker exec -it <attacker_container_name> /bin/bash

# Run the packet sniffer
python3 sniffer.py
```

### 2. Traffic Generation (Victim)
While the sniffer is running in the attacker node, use the victim node to generate traffic.

```bash
# Exec into the victim container in a new terminal
docker exec -it <victim_container_name> /bin/bash

# Trigger network traffic
python3 generate_traffic.py
```
*Switch back to the attacker terminal to analyze the intercepted network packets in real-time.*

## 📂 Project Structure

```text
.
├── docker-compose.yml     # Orchestrates the containers, network, and volumes
├── Dockerfile.attacker    # Docker configuration for the attacker node
├── Dockerfile.victim      # Docker configuration for the victim node
├── Dockerfile.http        # Docker configuration for the HTTP server
├── Dockerfile.telnet      # Docker configuration for the Telnet server
├── generate_traffic.py    # Script simulating user network activity (Victim)
├── http_server.py         # Simple HTTP server implementation
├── sniffer.py             # Custom network sniffer script (Attacker)
└── README.md              # Project documentation
```

## ⚠️ Disclaimer
**Educational Purposes Only:** This project is strictly for academic learning, researching network protocols, and understanding defensive computer security. Do not use the scripts, configurations, or techniques described here on any network or system where you do not have explicit permission.
