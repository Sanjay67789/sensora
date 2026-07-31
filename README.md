<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Sensora&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Discover%20•%20Identify%20•%20Diagnose%20•%20Monitor&descAlignY=58&descSize=20" width="100%"/>

<a href="https://github.com/Sanjay67789/sensora">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=38BDF8&center=true&vCenter=true&width=650&lines=Open-Source+Hardware+Discovery+Framework;Diagnose+I%C2%B2C+%7C+SPI+%7C+UART+%7C+1-Wire+devices;Built+for+Embedded+Linux;Raspberry+Pi+%E2%80%A2+Jetson+%E2%80%A2+BeagleBone+%E2%80%A2+SBCs" alt="Typing SVG" />
</a>

<br/>

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-Embedded-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img src="https://img.shields.io/badge/License-Apache%202.0-D22128?style=for-the-badge&logo=apache&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Pre--Alpha-orange?style=for-the-badge" />
</p>
<p>
  <img src="https://img.shields.io/badge/Architecture-ARM%20%7C%20x86__64-2ea44f?style=for-the-badge" />
  <img src="https://img.shields.io/badge/CLI-Typer-5A45FF?style=for-the-badge" />
  <img src="https://img.shields.io/github/stars/Sanjay67789/sensora?style=for-the-badge&color=yellow" />
</p>

</div>

<br/>

Sensora is a modern, open-source hardware discovery, identification, diagnostics, and management framework for Embedded Linux — unifying what usually takes five different tools into one extensible CLI.

<br/>

⚠️ Pre-Alpha Notice

Sensora is under active development. APIs, commands, and the device database may change before the first stable release.

📚 Table of Contents

<table>
<tr>
<td valign="top" width="33%">

🔍 Overview

## 🤔 Why Sensora?

Most Linux hardware utilities solve **one problem well**. Sensora combines discovery, identification, diagnostics and reporting into a single framework.

| Tool | Discover | Identify | Diagnose | Reports |
|------|:--------:|:--------:|:--------:|:-------:|
| `i2cdetect` | ✅ | ❌ | ❌ | ❌ |
| `i2c-tools` | ✅ | ❌ | ❌ | ❌ |
| `lm-sensors` | ⚠️ | ✅ | ✅ | ❌ |
| Linux IIO | ✅ | ⚠️ | ❌ | ❌ |
| **Sensora** | ✅ | ✅ | ✅ | ✅ |

> **One framework. One CLI. Multiple hardware buses.**
## ## ✨ Features

### 🔍 Hardware Discovery
- Automatic device discovery
- Multi-bus scanning
- Linux hardware abstraction
- Raspberry Pi & Embedded Linux support

### 🧠 Intelligent Identification
**Available**
- Address matching
- Device database
- Unknown device detection

**Planned**
- Register fingerprinting
- Chip-ID verification
- Confidence scoring

### 🩺 Diagnostics
- Bus validation
- Health checks
- Communication diagnostics
- Error reporting

### 📊 Reporting
- System summary
- Hardware inventory
- Health reports
- Database statistics
## ## 🔌 Supported Buses

| Bus | Support |
|------|---------|
| I²C | ✅ |
| SPI | ✅ |
| UART | ✅ |
| 1-Wire | ✅ |
| GPIO | 🚧 |
| USB | 🚧 |
| CAN | 🚧 |
| HID | 🚧 |
| Bluetooth | 🚧 |
| Modbus | 🚧 |
## ⚙️ Installation

⚙️ Installation

🚀 Quick Start

🖥️ Example Output

## 🏗️ Architecture

```mermaid
flowchart LR
    A[Hardware Discovery] --> B[Bus Layer]
    B --> C[Device Enumeration]
    C --> D[Device Matcher]
    D --> E[Diagnostics]
    E --> F[Health Assessment]
    F --> G[Reports]
```
## ## 📁 Project Structure

```text
sensora/
├── buses/
├── commands/
├── core/
├── database/
├── definitions/
├── diagnostics/
├── discovery/
├── reports/
├── utils/
├── cli.py
└── pyproject.toml
```
## 📌 Development Status

📌 Development Status

🗺️ Roadmap

🤝 Contributing

</td>
</tr>
</table>

<br/>

🔍 Overview

Sensora is an open-source hardware discovery, identification, diagnostics, and management framework designed for Linux-based embedded systems.

It automatically discovers hardware connected through multiple communication buses, intelligently identifies devices using hardware-aware detection techniques, validates communication, performs diagnostics, and generates detailed hardware reports.

Unlike traditional Linux utilities that focus on a single task, Sensora provides a unified framework for hardware inspection and diagnostics.

<br/>

<div align="center">

🎯 Designed For









🍓 Raspberry Pi

🟢 NVIDIA Jetson

🍊 Orange Pi

🐝 BeagleBone

🪨 Rock Pi

🏭 Industrial SBCs

🚗 Automotive Prototypes

📡 IoT Gateways

🤖 Robotics

🐧 Embedded Linux Dev

🧪 Hardware Validation & Testing



</div>

<br/>

🤔 Why Sensora?

Most Linux hardware tools solve only one part of the problem — Sensora brings them together.

<div align="center">

Tool

Discovery

Identification

Diagnostics

Reports

i2cdetect

✅

❌

❌

❌

i2c-tools

✅

❌

❌

❌

lm-sensors

⚠️

✅

✅

❌

Linux IIO

✅

⚠️

❌

❌

Sensora

✅

✅

✅

✅

</div>

<br/>

✨ Features

<table>
<tr>
<td width="50%" valign="top">

🔎 Hardware Discovery

Automatic device discovery

Multi-bus scanning

Linux hardware abstraction

Fast scanning engine

Embedded Linux support

Raspberry Pi optimized

</td>
<td width="50%" valign="top">

🧠 Intelligent Identification

Available now

Device database

Address matching

Unknown device detection

Coming soon

Register fingerprinting

Chip ID verification

Confidence scoring

</td>
</tr>
<tr>
<td width="50%" valign="top">

🩺 Diagnostics

Bus validation

Hardware health checks

Communication diagnostics

Device availability checks

Error reporting

Hardware inspection

</td>
<td width="50%" valign="top">

📊 Reporting

System information

Hardware inventory

Device status

Health summary

Database statistics

Bus information

</td>
</tr>
</table>

<br/>

🔌 Supported Buses

<div align="center">

Bus

Status

I²C

✅ Supported

SPI

✅ Supported

UART

✅ Supported

1-Wire

✅ Supported

GPIO

🚧 Planned

USB

🚧 Planned

CAN

🚧 Planned

HID

🚧 Planned

Bluetooth

🚧 Planned

Modbus

🚧 Planned

</div>

<br/>

⚙️ Installation

1. Clone the repository

git clone https://github.com/Sanjay67789/sensora.git
cd sensora

2. Create a virtual environment

python3 -m venv .venv
source .venv/bin/activate

3. Install

pip install -e .

<br/>

🚀 Quick Start

<table>
<tr><th align="left">Command</th><th align="left">Description</th></tr>
<tr><td>

sensora info

</td><td>Display system information</td></tr>
<tr><td>

sensora scan

</td><td>Scan hardware</td></tr>
<tr><td>

sensora scan --bus i2c --verbose

</td><td>Verbose I²C scan</td></tr>
<tr><td>

sensora doctor

</td><td>Run diagnostics</td></tr>
<tr><td>

sensora report

</td><td>Generate full report</td></tr>
<tr><td>

sensora report --quick

</td><td>Generate quick report</td></tr>
<tr><td>

sensora devices

</td><td>List supported devices</td></tr>
</table>

<br/>

🖥️ Example Output

<details open>
<summary><b>🔍 Scan</b></summary>

$ sensora scan --bus i2c --verbose

Found 3 device(s)

[1] Unknown I²C Device
    Address : 0x30

[2] Unknown I²C Device
    Address : 0x37

[3] Unknown I²C Device
    Address : 0x50

</details>

<details>
<summary><b>📊 Report</b></summary>

$ sensora report

System
--------
OS           : Linux
Kernel       : 6.x
Python       : 3.11+

Database
--------
Devices : 38

Detected Hardware
-----------------
3 I²C Devices

Health Summary
--------------
GOOD WITH WARNINGS

</details>

<br/>

🏗️ Architecture

%%{init: {
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#1f2937",
    "primaryTextColor": "#f9fafb",
    "primaryBorderColor": "#38bdf8",
    "lineColor": "#38bdf8",
    "secondaryColor": "#0f172a",
    "tertiaryColor": "#111827",
    "fontFamily": "Fira Code, monospace"
  }
}}%%
flowchart TD
    A(["🧭 Hardware Discovery"]):::start --> B["🔌 Bus Abstraction Layer<br/><sub>I²C • SPI • UART • 1-Wire</sub>"]:::core
    B --> C["📋 Device Enumeration"]:::core
    C --> D{"🧠 Intelligent Identification<br/><sub>Address • Registers • Chip IDs</sub>"}:::brain
    D --> E["🩺 Diagnostics & Validation"]:::diag
    E --> F["❤️ Health Assessment"]:::health
    F --> G(["📊 Reports & Future Automation"]):::finish

    classDef start fill:#0ea5e9,stroke:#38bdf8,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef core fill:#1e293b,stroke:#38bdf8,stroke-width:1.5px,color:#e2e8f0
    classDef brain fill:#7c3aed,stroke:#a78bfa,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef diag fill:#f59e0b,stroke:#fbbf24,stroke-width:1.5px,color:#111827
    classDef health fill:#ef4444,stroke:#f87171,stroke-width:1.5px,color:#ffffff
    classDef finish fill:#22c55e,stroke:#4ade80,stroke-width:2px,color:#052e16,font-weight:bold

<sub>💡 GitHub renders Mermaid diagrams natively — this flow updates live as the pipeline evolves.</sub>

<br/>

📁 Project Structure

sensora/
├── buses/          # I²C, SPI, UART, 1-Wire backends
├── commands/        # CLI command implementations
├── core/             # Core framework logic
├── database/          # Device database
├── definitions/         # Bus & device definitions
├── diagnostics/           # Health checks & validation
├── discovery/               # Hardware discovery engine
├── reports/                   # Report generation
├── utils/                       # Shared utilities
├── cli.py                         # CLI entry point
├── pyproject.toml
└── README.md

<br/>

📌 Development Status

<div align="center">

Current Release: 🟠 Pre-Alpha

</div>

<table>
<tr>
<td width="50%" valign="top">

✅ Implemented

Linux bus abstraction

CLI

I²C scanning

SPI scanning

UART scanning

1-Wire scanning

Device database

Intelligent matcher

Diagnostics

Report generation

Raspberry Pi support

Generic Embedded Linux support

</td>
<td width="50%" valign="top">

🚧 In Development

Register fingerprinting

Chip ID verification

Detector plugins

Improved matching engine

Vendor-specific identification

Hardware validation

</td>
</tr>
</table>

<br/>

🗺️ Roadmap

<table>
<tr><th>Version</th><th>Milestones</th></tr>
<tr>
<td><b>v0.1</b> ✅</td>
<td>CLI • Multi-bus discovery • Device database • Diagnostics • Reports</td>
</tr>
<tr>
<td><b>v0.2</b> 🚧</td>
<td>Register fingerprinting • Chip ID verification • EEPROM detection • Confidence scoring • Detector plugins</td>
</tr>
<tr>
<td><b>v0.3</b> 🔜</td>
<td>MQTT integration • JSON / HTML / YAML reports • Plugin SDK • Live monitoring</td>
</tr>
<tr>
<td><b>v1.0</b> 🎯</td>
<td>Stable API • Extensive hardware database • Production-ready docs • Hundreds of supported devices • Plugin ecosystem</td>
</tr>
</table>

<br/>

🎯 Design Goals

<div align="center">

Lightweight • Fast • Extensible • Vendor-independent • Hardware-aware • Scriptable • Production-ready • Embedded-first

</div>

<br/>

🌟 Key Highlights

Unified hardware discovery framework for Embedded Linux

Intelligent device identification (address, register and chip-ID based)

Multi-bus architecture with an extensible plugin design

Designed for Raspberry Pi, SBCs, robotics, automotive and industrial systems

Modern Python codebase with type hints and clean architecture

🔭 Vision

Sensora aims to become the standard open-source hardware discovery and diagnostics framework for Embedded Linux — supporting hundreds of sensors, EEPROMs, ADCs, DACs, GPIO expanders, displays, communication modules, industrial peripherals, and automotive hardware through an extensible detector architecture.

<br/>

🛠️ Development

Sensora follows modern Python development practices:

<div align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Type_Hinted-✔-2ea44f?style=flat-square" />
<img src="https://img.shields.io/badge/Linting-Ruff-D7FF64?style=flat-square" />
<img src="https://img.shields.io/badge/Formatting-Black-000000?style=flat-square" />
<img src="https://img.shields.io/badge/Testing-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" />
<img src="https://img.shields.io/badge/Versioning-SemVer-e10098?style=flat-square" />

</div>

<br/>

🤝 Contributing

Contributions are welcome! Areas where you can help:

🔌 Hardware detectors

🚌 Bus implementations

🩺 Diagnostics

📖 Documentation

🧪 Unit tests

💡 Examples

⚡ Performance improvements

Please open an issue before implementing major changes.

<br/>

📄 License

Copyright © 2026 Sanjay Kumar P
Licensed under the Apache License 2.0.

See the LICENSE file for details.

<br/>

👤 Author

<div align="center">

<img src="https://img.shields.io/badge/Sanjay_Kumar_P-Electronics_%26_Communication_Engineering-1e293b?style=for-the-badge&logo=github&logoColor=white" />

Embedded Systems • Linux • IoT • Hardware Diagnostics

<a href="https://github.com/Sanjay67789">
  <img src="https://img.shields.io/badge/GitHub-@Sanjay67789-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>

</div>

<br/>

<div align="center">

⭐ If you find Sensora useful, please consider giving the repository a star.

Built with ❤️ for the Embedded Linux community.

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>

❤️ Acknowledgements

Sensora is an independent open-source project created and maintained by Sanjay Kumar P.

Special thanks to the Embedded Linux and Python open-source communities whose libraries, tools, and documentation have inspired this project.

📈 Project Goals

Become the standard hardware discovery framework for Embedded Linux.

Support hundreds of sensors and peripherals.

Provide a stable API for developers and integrators.

Enable automated diagnostics and monitoring workflows.
