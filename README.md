# Sensora

> Discover • Identify • Diagnose • Monitor

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Platform](https://img.shields.io/badge/Linux-Embedded-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Pre--Alpha-orange)

Sensora is an open-source hardware discovery, diagnostics, and management framework for Linux-based embedded systems.

It automatically discovers devices connected through buses such as **I²C, SPI, UART, 1-Wire, GPIO, USB, and CAN**, identifies them using intelligent detection techniques, performs diagnostics, and generates detailed hardware reports.

Sensora is designed for Raspberry Pi, industrial SBCs, IoT gateways, robotics, automotive prototypes, embedded Linux development, and hardware validation.

---

# Why Sensora?

Most Linux tools only solve one part of the problem.

| Tool | Discovery | Identification | Diagnostics | Reports |
|------|:---------:|:--------------:|:-----------:|:-------:|
| i2cdetect | ✅ | ❌ | ❌ | ❌ |
| i2c-tools | ✅ | ❌ | ❌ | ❌ |
| lm-sensors | ⚠️ | ✅ | ✅ | ❌ |
| Linux IIO | ✅ | ⚠️ | ❌ | ❌ |
| Sensora | ✅ | ✅ | ✅ | ✅ |

Sensora combines hardware discovery, intelligent identification, diagnostics, and reporting into a single extensible framework.

---

# Features

## Hardware Discovery

- Automatic device discovery
- Multi-bus scanning
- Linux hardware abstraction
- Fast scanning engine
- Raspberry Pi support
- Generic embedded Linux support

Supported buses

- ✅ I²C
- ✅ SPI
- ✅ UART
- ✅ 1-Wire

Planned

- GPIO
- USB
- CAN
- HID
- Bluetooth
- Modbus

---

## Intelligent Device Identification

Current

- Address matching
- Device database
- Unknown device detection

Next Generation

- Register fingerprinting
- Chip ID verification
- Device confidence scoring
- Vendor-specific detectors
- Automatic register probing

Instead of only matching an I²C address, Sensora aims to identify devices using hardware fingerprints and register verification.

---

## Diagnostics

- Hardware health checks
- Bus validation
- Communication diagnostics
- Device availability
- Error reporting

---

## Reports

Generate comprehensive reports containing

- System information
- Hardware inventory
- Device status
- Health summary
- Database statistics
- Bus information

---

# Quick Start

Clone the repository

```bash
git clone https://github.com/Sanjay67789/sensora.git
cd sensora
```

Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install

```bash
pip install -e .
```

---

# Commands

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

# Current Status

**Development Stage:** Pre-Alpha

Implemented

- Linux bus abstraction
- CLI
- I²C scanning
- SPI scanning
- UART scanning
- 1-Wire scanning
- Device database
- Diagnostics
- Report generation
- Raspberry Pi support
- Generic Linux support

In Progress

- Register fingerprinting
- Device detector plugins
- Improved matching engine
- Sensor validation
- Vendor-specific identification

---

# Architecture

```
                Sensora

          Hardware Discovery
                  │
                  ▼
           Bus Abstraction
                  │
                  ▼
          Device Detection
                  │
                  ▼
      Register Fingerprinting
                  │
                  ▼
       Intelligent Identification
                  │
                  ▼
         Diagnostics & Health
                  │
                  ▼
              Reports
```

---

# Project Structure

```
sensora/
├── buses/
├── commands/
├── core/
├── database/
├── definitions/
├── diagnostics/
├── discovery/
├── plugins/
├── reports/
├── utils/
└── cli.py
```

---

# Roadmap

## Version 0.1

- ✅ CLI
- ✅ Hardware discovery
- ✅ Multi-bus architecture
- ✅ Device database
- ✅ Diagnostics
- ✅ Reports

## Version 0.2

- Register fingerprinting
- Chip ID verification
- Detector plugins
- Confidence scoring
- EEPROM support

## Version 0.3

- Live monitoring
- MQTT integration
- JSON reports
- HTML reports
- Plugin SDK

## Version 1.0

- Stable API
- Extensive sensor library
- Automated diagnostics
- Production-ready documentation

---

# Supported Platforms

- Raspberry Pi
- NVIDIA Jetson
- Orange Pi
- BeagleBone
- Rock Pi
- Generic Embedded Linux
- Industrial SBCs

---

# Vision

Sensora aims to become the **standard open-source hardware discovery and diagnostics framework for embedded Linux**.

The long-term goal is to support hundreds of sensors, EEPROMs, ADCs, DACs, GPIO expanders, displays, communication modules, and industrial peripherals through an extensible detector and plugin architecture.

---

# Development

Sensora follows modern Python development practices.

- Python 3.11+
- Type hints
- Ruff
- Black
- Pytest
- MIT License

---

# Contributing

Contributions are welcome.

You can contribute by adding:

- Sensor detectors
- Bus implementations
- Diagnostics
- Documentation
- Tests
- Examples

---

# Author

**Sanjay Kumar P**

Electronics & Communication Engineering

Embedded Systems • Linux • IoT • Hardware Diagnostics

GitHub: https://github.com/Sanjay67789

---

⭐ If you find Sensora useful, consider starring the repository to support its development.
