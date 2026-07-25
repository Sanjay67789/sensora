# Sensora

> Embedded Hardware Discovery, Diagnostics & Management Framework

Sensora is an open-source Python framework for discovering, identifying, and diagnosing hardware devices connected to embedded Linux systems.

It is designed for Raspberry Pi, industrial SBCs, development boards, IoT gateways, and custom Linux-based embedded devices.

---

## Features

- 🔍 Automatic hardware discovery
- 📡 Multi-bus support
  - I²C
  - SPI
  - UART
  - USB
  - GPIO
  - (More buses planned)
- 🧠 Device identification using a built-in database
- 🩺 Hardware diagnostics and health checks
- 📄 Report generation
- 🔌 Plugin architecture for custom buses and vendors
- 🖥️ Modern command-line interface

---

## Project Status

> **Current Stage:** Early Development

The project architecture has been completed and core functionality is currently under active development.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Sanjay67789/sensora.git
cd sensora
```

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -e .
```

---

## Planned Commands

```bash
sensora scan
sensora doctor
sensora info
sensora report
sensora list buses
sensora list devices
```

---

## Project Structure

```text
sensora/
├── buses/          # Bus implementations
├── commands/       # CLI commands
├── core/           # Core domain models
├── database/       # Device database
├── diagnostics/    # Health checks
├── discovery/      # Discovery engine
├── plugins/        # Plugin API
└── utils/          # Shared utilities
```

---

## Roadmap

### Phase 1
- [x] Project setup
- [x] GitHub repository
- [x] Packaging
- [x] Project architecture

### Phase 2
- [ ] Core device model
- [ ] Bus abstraction
- [ ] Discovery engine
- [ ] Device database

### Phase 3
- [ ] I²C support
- [ ] SPI support
- [ ] UART support
- [ ] USB support

### Phase 4
- [ ] Diagnostics
- [ ] Report generation
- [ ] Plugin SDK
- [ ] Documentation

---

## Target Platforms

- Raspberry Pi
- NVIDIA Jetson
- BeagleBone
- Orange Pi
- Rock Pi
- Generic Linux Embedded Systems

---

## Development

This project follows:

- Python 3.11+
- Type hints
- Black
- Ruff
- Pytest

Contributions are welcome once the core framework reaches its first stable milestone.

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## Author

**Sanjay Kumar P**

GitHub: https://github.com/Sanjay67789
