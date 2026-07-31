<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Sensora&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Discover%20•%20Identify%20•%20Diagnose%20•%20Monitor&descAlignY=58&descSize=20" width="100%"/>

<a href="https://github.com/Sanjay67789/sensora">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=38BDF8&center=true&vCenter=true&width=650&lines=Open-Source+Hardware+Discovery+Framework;Diagnose+I%C2%B2C+%7C+SPI+%7C+UART+%7C+1-Wire+devices;Built+for+Embedded+Linux" alt="Typing SVG" />
</a>

A modern open-source hardware discovery, diagnostics, and management framework for Embedded Linux.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Platform](https://img.shields.io/badge/Linux-Embedded-success)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)
![Status](https://img.shields.io/badge/Status-Pre--Alpha-orange)
![Architecture](https://img.shields.io/badge/Architecture-ARM%20%7C%20x86__64-success)
![CLI](https://img.shields.io/badge/CLI-Typer-blueviolet)

</div>

---

## Overview

Sensora is an open-source hardware discovery, identification, diagnostics, and management framework designed for Linux-based embedded systems.

It automatically discovers hardware connected through multiple communication buses, intelligently identifies devices using hardware-aware detection techniques, validates communication, performs diagnostics, and generates detailed hardware reports.

Unlike traditional Linux utilities that focus on a single task, Sensora provides a unified framework for hardware inspection and diagnostics.

### Designed For

- Raspberry Pi
- NVIDIA Jetson
- Orange Pi
- BeagleBone
- Rock Pi
- Industrial SBCs
- Automotive prototypes
- IoT gateways
- Robotics
- Embedded Linux development
- Hardware validation and testing

---

# Table of Contents

- Overview
- Why Sensora?
- Features
- Supported Hardware
- Installation
- Quick Start
- CLI Commands
- Example Output
- Architecture
- Project Structure
- Development Status
- Roadmap
- Contributing
- License
- Author

---

# Why Sensora?

Most Linux hardware tools solve only one part of the problem.

| Tool | Discovery | Identification | Diagnostics | Reports |
|------|:---------:|:--------------:|:-----------:|:-------:|
| i2cdetect | ✅ | ❌ | ❌ | ❌ |
| i2c-tools | ✅ | ❌ | ❌ | ❌ |
| lm-sensors | ⚠️ | ✅ | ✅ | ❌ |
| Linux IIO | ✅ | ⚠️ | ❌ | ❌ |
| Sensora | ✅ | ✅ | ✅ | ✅ |

Sensora combines discovery, identification, diagnostics, and reporting into one extensible framework.

---

# Features

## Hardware Discovery

- Automatic device discovery
- Multi-bus scanning
- Linux hardware abstraction
- Fast scanning engine
- Embedded Linux support
- Raspberry Pi optimized

---

## Intelligent Identification

Current capabilities

- Device database
- Address matching
- Unknown device detection

Planned capabilities

- Register fingerprinting
- Chip ID verification
- Vendor-specific detectors
- Automatic register probing
- Confidence scoring
- Intelligent identification engine

---

## Diagnostics

- Bus validation
- Hardware health checks
- Communication diagnostics
- Device availability
- Error reporting
- Hardware inspection

---

## Reporting

Generate comprehensive reports containing

- System information
- Hardware inventory
- Device status
- Health summary
- Database statistics
- Bus information

---

# Supported Buses

| Bus | Status |
|------|--------|
| I²C | ✅ Supported |
| SPI | ✅ Supported |
| UART | ✅ Supported |
| 1-Wire | ✅ Supported |
| GPIO | 🚧 Planned |
| USB | 🚧 Planned |
| CAN | 🚧 Planned |
| HID | 🚧 Planned |
| Bluetooth | 🚧 Planned |
| Modbus | 🚧 Planned |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Sanjay67789/sensora.git

cd sensora
```

## Create Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

## Install

```bash
pip install -e .
```

---

# Quick Start

Display system information

```bash
sensora info
```

Scan hardware

```bash
sensora scan
```

Verbose I²C scan

```bash
sensora scan --bus i2c --verbose
```

Run diagnostics

```bash
sensora doctor
```

Generate report

```bash
sensora report
```

Quick report

```bash
sensora report --quick
```

List supported devices

```bash
sensora devices
```

---

# Example

## Scan

```text
$ sensora scan --bus i2c --verbose

Found 3 device(s)

[1] Unknown I²C Device
    Address : 0x30

[2] Unknown I²C Device
    Address : 0x37

[3] Unknown I²C Device
    Address : 0x50
```

---

## Report

```text
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
```

---

# Architecture

```text
                      Sensora

               Hardware Discovery
                      │
                      ▼
              Bus Abstraction Layer
                      │
                      ▼
              Device Enumeration
                      │
                      ▼
         Intelligent Identification
   (Address • Registers • Chip IDs)
                      │
                      ▼
           Diagnostics & Validation
                      │
                      ▼
              Health Assessment
                      │
                      ▼
           Reports & Future Automation
```

---

# Project Structure

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
├── pyproject.toml
└── README.md
```

---

# Development Status

**Current Release**

**Pre-Alpha**

Implemented

- Linux bus abstraction
- CLI
- I²C scanning
- SPI scanning
- UART scanning
- 1-Wire scanning
- Device database
- Intelligent matcher
- Diagnostics
- Report generation
- Raspberry Pi support
- Generic Embedded Linux support

Currently in development

- Register fingerprinting
- Chip ID verification
- Detector plugins
- Improved matching engine
- Vendor-specific identification
- Hardware validation

---

# Roadmap

## Version 0.1

- ✅ CLI
- ✅ Multi-bus discovery
- ✅ Device database
- ✅ Diagnostics
- ✅ Reports

---

## Version 0.2

- Register fingerprinting
- Chip ID verification
- EEPROM detection
- Confidence scoring
- Detector plugins

---

## Version 0.3

- MQTT integration
- JSON reports
- HTML reports
- YAML reports
- Plugin SDK
- Live monitoring

---

## Version 1.0

- Stable API
- Extensive hardware database
- Production-ready documentation
- Hundreds of supported devices
- Automated diagnostics
- Plugin ecosystem

---

# Design Goals

- Lightweight
- Fast
- Extensible
- Vendor-independent
- Hardware-aware
- Scriptable
- Production-ready
- Embedded-first

---

# Vision

Sensora aims to become the standard open-source hardware discovery and diagnostics framework for Embedded Linux.

The long-term objective is to support hundreds of sensors, EEPROMs, ADCs, DACs, GPIO expanders, displays, communication modules, industrial peripherals, and automotive hardware through an extensible detector architecture.

---

# Development

Sensora follows modern Python development practices.

- Python 3.11+
- Fully type hinted
- Ruff
- Black
- Pytest
- Semantic Versioning
- Apache License 2.0

---

# Contributing

Contributions are welcome.

Areas where you can help include:

- Hardware detectors
- Bus implementations
- Diagnostics
- Documentation
- Unit tests
- Examples
- Performance improvements

Please open an issue before implementing major changes.

---

# License

Copyright © 2026 Sanjay Kumar P

Licensed under the Apache License 2.0.

See the **LICENSE** file for details.

---

# Author

**Sanjay Kumar P**

Electronics & Communication Engineering

Embedded Systems • Linux • IoT • Hardware Diagnostics

GitHub

https://github.com/Sanjay67789

---

<div align="center">

### ⭐ If you find Sensora useful, please consider giving the repository a star.

Built with ❤️ for the Embedded Linux community.

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>
