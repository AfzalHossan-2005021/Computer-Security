<div align="center">
  <h1>🛡️ Computer Security (CSE 405 & CSE 406)</h1>
  <p><i>Comprehensive repository of academic coursework, assignments, and practical exploits focusing on applied computer and network security.</i></p>
  
  ![Institution](https://img.shields.io/badge/Institution-BUET-blue.svg?style=flat-square)
  ![Level](https://img.shields.io/badge/Level-4%2FTerm--1-success.svg?style=flat-square)
  ![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
  ![C](https://img.shields.io/badge/C-GNU-blue?style=flat-square&logo=c)
  ![Docker](https://img.shields.io/badge/Docker-Containers-blue?style=flat-square&logo=docker)
</div>

## 📖 Overview
This repository serves as a centralized portfolio of works completed for the **CSE 405 (Computer Security)** and **CSE 406 (Computer Security Sessional)** courses at the Department of Computer Science and Engineering, Bangladesh University of Engineering and Technology (CSE BUET). The curriculum encompasses a broad spectrum of security domains including applied cryptography, memory corruption vulnerabilities, web application security, and network protocol analysis.

---

## 📋 Table of Contents
1. [Overview](#-overview)
2. [Repository Architecture](#-repository-architecture)
3. [Technologies & Tools](#-technologies--tools)
4. [Disclaimer](#-disclaimer)

---

## 🏗️ Repository Architecture

### 1. [Applied Cryptography (`./Assignment-01/`)](./Assignment-01/)
Implementation of industry-standard cryptographic algorithms and secure communication channels.
* **Symmetric Cryptography:** Complete implementation of AES (Advanced Encryption Standard) with customizable key streams utilizing the `BitVector` library.
* **Asymmetric Cryptography:** Elliptic Curve Cryptography (ECC) module featuring a secure message exchange simulation between distinct sender and receiver nodes.

### 2. [Authentication & Web Analysis (`./Assignment-02/`)](./Assignment-02/)
Exploration of modern authentication paradigms incorporating behavioral biometrics and machine learning.
* Features data collection pipelines (`collect.py`), localized storage (`database.py`), and machine learning model training (`train.py`) utilizing dynamic JavaScript Web Workers.

### 3. [Memory Corruption Exploitation (`./Online-01/`)](./Online-01/)
Low-level systems security focusing on binary exploitation and mitigation circumvention.
* **Buffer Overflows:** Practical exploitation of stack vulnerabilities in C binaries. Includes memory layout analysis via GDB and custom Python-based exploit scaffolding (`exploit.py`) to bypass standard compiler protections.

### 4. [Web Application Vulnerabilities (`./Online-02/`)](./Online-02/)
Identification and exploitation of generic web application vulnerabilities focusing strictly on database layers.
* **SQL Injection (SQLi):** Demonstrations utilizing a modernized configuration of `sqli-labs`, evaluating various attack vectors (Union-based, Error-based, Blind) and defensive coding strategies in PHP/MySQL environments.

### 5. [Network Security Sandbox (`./Project/`)](./Project/)
A sophisticated, containerized laboratory environment for analyzing network telemetry and protocol vulnerabilities.
* **Topology:** Isolated Docker containers mapping distinct network entities (Attacker, Victim, HTTP Service, Telnet Service).
* **Analysis:** Includes programmatic traffic generation and Python-based packet sniffing capabilities to demonstrate clear-text protocol interception and active Machine-in-the-Middle (MITM) contexts.

---

## ⚙️ Technologies & Tools

| Category | Utilities |
|:---|:---|
| **Programming Languages** | Python, C, JavaScript, PHP, Bash |
| **Virtualization & DevOps** | Docker, Docker Compose |
| **Security & Analysis Tools** | GDB (GNU Debugger), Advanced Network Analyzers |
| **Core Concepts** | Cryptography, Binary Exploitation, SQL Injection, Packet Sniffing |

---

## ⚠️ Disclaimer

**Educational Purposes Only.** All materials, exploit scripts, and network sandbox configurations provided within this repository are strictly for academic and educational purposes. The code demonstrates the mechanics of software vulnerabilities to foster a better understanding of system defenses and secure coding practices. Do not utilize any of these techniques against infrastructure or systems for which you do not have explicit, localized authorization.
