# Wake-on-LAN Script with YAML Configuration

This Python script provides a simple way to power on computers remotely using **Wake-on-LAN (WOL)**. It allows you to store multiple computer configurations in a YAML file and wake them up by name.

## How It Works

The script sends a **Magic Packet** to a target computer’s MAC address. This packet tells the computer’s network card to wake up, as long as Wake-on-LAN is enabled in its BIOS and network settings.

The main steps are:

1. Read a YAML configuration file (default: `~/.wol.yaml`).
2. Select a computer by name from the configuration.
3. Send a Magic Packet with the computer’s MAC address, broadcast address, and port.

## YAML Configuration

Each computer is defined in the YAML file with three fields:

* `mac`: The MAC address of the network card.
* `broadcast`: (Optional) Broadcast address, default is `255.255.255.255`.
* `port`: (Optional) UDP port, default is `9`.

Example `.wol.yaml`:

```yaml
desktop:
  mac: "00:11:22:33:44:55"
  broadcast: "192.168.1.255"
  port: 9

server:
  mac: "66:77:88:99:AA:BB"
```

## Usage

* List available computers:

  ```bash
  python3 wol.py -l
  ```
* Wake up a computer by name:

  ```bash
  python3 wol.py desktop
  ```

## Why Use It?

This script is useful for:

* Managing multiple computers from a single configuration file.
* Avoiding the need to remember long MAC addresses.
* Quickly waking up servers, desktops, or media PCs over the network.
