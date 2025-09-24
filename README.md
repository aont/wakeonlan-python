# Wake-on-LAN Script with YAML Configuration, Interface Control, and Flexible Options

This Python script provides a **powerful and flexible tool** to wake computers remotely using **Wake-on-LAN (WOL)**. Unlike basic implementations, it supports:

* **Direct MAC input** without configuration files
* **Network interface selection** for precise control
* **Multiple machine configurations** stored in YAML
* **Diagnostic features** such as listing available interfaces and configured machines

## Installation

Install the latest version directly from GitHub using pip:

```bash
pip install git+https://github.com/aont/wakeonlan-python.git
```

After installation the command-line entry point is available as `wakeonlan` (an alias `wakeonlan-python` is also installed).

---

## Features at a Glance

* Send **Magic Packets** to wake systems by **name**, **MAC address**, or **YAML configuration**.
* Specify **broadcast addresses**, **UDP ports**, and **network interfaces**.
* Manage multiple hosts from a **single configuration file**.
* Built-in tools to **list available network interfaces** and **configured machines**.
* Support for **default settings** shared across all hosts in YAML.

---

## How It Works

1. **YAML configuration loading** (default: `~/.wol.yaml`) with support for global defaults.
2. **Target selection** by friendly name, MAC address, or command-line options.
3. **Network interface binding** to ensure the packet is sent from the correct adapter.
4. **Magic Packet generation and transmission**, repeated across available IPv4 interfaces if needed.

If the target computer has Wake-on-LAN enabled in its BIOS/UEFI and operating system settings, it will power on when it receives the packet.

---

## YAML Configuration

Each entry in the YAML file can include:

* **`mac`** (required): Target machine’s MAC address.
* **`broadcast`** (optional): Broadcast address (default: `255.255.255.255`).
* **`port`** (optional): UDP port (default: `9`).
* **`interface`** (optional): Network interface to use (default: all available IPv4 interfaces).

### Example `.wol.yaml`

```yaml
@default:
  broadcast: "192.168.1.255"
  port: 9

desktop:
  mac: "00:11:22:33:44:55"
  interface: "eth0"

server:
  mac: "66:77:88:99:AA:BB"
```

In this example, the `server` entry inherits default values for `broadcast` and `port`.

---

## Usage Examples

### List Available Computers

Show all configured machines from the YAML file:

```bash
wakeonlan -l
```

### List Network Interfaces

Display all IPv4-enabled interfaces available for packet transmission:

```bash
wakeonlan --list-interfaces
```

### Wake a Machine by Name (YAML Config)

Wake a target defined in the YAML file:

```bash
wakeonlan desktop
```

### Wake a Machine by Direct MAC Input

Wake a machine without using YAML:

```bash
wakeonlan --mac 00:11:22:33:44:55
```

You can also specify custom options:

```bash
wakeonlan --mac 00:11:22:33:44:55 \
               --broadcast 192.168.1.255 \
               --port 7 \
               --interface eth0
```

### Use a Custom YAML Config File

Provide a non-default YAML configuration file:

```bash
wakeonlan -c ./my_wol.yaml server
```

---

## Why This Script?

This script is ideal for **home labs, servers, and remote work setups** where multiple machines need to be managed efficiently.

* **Centralized management**: Keep all machine definitions in a YAML file.
* **Direct control**: Send packets quickly without a config file.
* **Ease of use**: Refer to machines by human-readable names instead of raw MACs.
* **Flexibility**: Choose specific interfaces, broadcasts, and ports.
* **Diagnostics**: Instantly view available interfaces and configurations.

---

⚡ With this script, waking your machines becomes **simple, flexible, and reliable**—whether you’re managing a single desktop or a fleet of servers.