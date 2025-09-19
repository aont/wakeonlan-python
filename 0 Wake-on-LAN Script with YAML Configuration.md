# Wake-on-LAN Script with YAML Configuration and Interface Support

This Python script provides a convenient way to power on computers remotely using **Wake-on-LAN (WOL)**. Unlike simpler scripts, it supports network interface selection and can manage multiple machine configurations through a YAML file.

---

## How It Works

The script generates and sends a **Magic Packet** to a target computer’s MAC address. If Wake-on-LAN is enabled in the computer’s BIOS/UEFI and network settings, the system will power on when the packet is received.

The main steps are:

1. Load a YAML configuration file (default: `~/.wol.yaml`).
2. Select a computer by name from the configuration.
3. Optionally, specify the network interface to send the packet from.
4. Send a Magic Packet containing the computer’s MAC address, broadcast address, and port.

---

## YAML Configuration

Each computer entry in the YAML file can define the following fields:

* **`mac`** (required): The MAC address of the network card.
* **`broadcast`** (optional): Broadcast address, defaults to `255.255.255.255`.
* **`port`** (optional): UDP port, defaults to `9`.
* **`interface`** (optional): The network interface name to use. If omitted, the script will attempt to send from all interfaces with an IPv4 address.

Example `.wol.yaml`:

```yaml
desktop:
  mac: "00:11:22:33:44:55"
  broadcast: "192.168.1.255"
  port: 9
  interface: "eth0"

server:
  mac: "66:77:88:99:AA:BB"
```

---

## Usage

### List Available Computers

Prints the configured machines and their settings:

```bash
python3 wol.py -l
```

### List Network Interfaces

Shows the local interfaces and IPv4 addresses available for sending packets:

```bash
python3 wol.py --list-interfaces
```

### Wake Up a Computer

Wakes up a machine by name (defined in the YAML file):

```bash
python3 wol.py desktop
```

### Specify a Custom Configuration File

Use a non-default YAML file:

```bash
python3 wol.py -c ./my_wol.yaml server
```

---

## Why Use This Script?

This script is useful for:

* **Centralized management**: Store multiple machine definitions in a single YAML file.
* **Ease of use**: Wake machines by their friendly names instead of remembering MAC addresses.
* **Flexibility**: Choose broadcast addresses, ports, and network interfaces when needed.
* **Diagnostics**: Quickly list available interfaces and configuration entries.
