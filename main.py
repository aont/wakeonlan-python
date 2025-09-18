#!/usr/bin/env python3
import socket
import argparse
import yaml
import sys
from pathlib import Path


def send_magic_packet(mac_address, broadcast="255.255.255.255", port=9):
    mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
    if len(mac_bytes) != 6:
        raise ValueError(f"Invalid MAC address format: {mac_address}")

    packet = b"\xFF" * 6 + mac_bytes * 16

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(packet, (broadcast, port))
    print(f"Magic Packet sent to {mac_address} via {broadcast}:{port}")


def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Failed to load YAML file: {e}")
        sys.exit(1)


def main():
    default_config = Path.home() / ".wol.yaml"

    parser = argparse.ArgumentParser(
        description="Wake-on-LAN using YAML configuration"
    )
    parser.add_argument(
        "name", nargs="?", help="Target computer name defined in YAML"
    )
    parser.add_argument(
        "-c", "--config", dest="config", default=str(default_config),
        help=f"YAML config file (default: {default_config})"
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="List available computers from config"
    )
    args = parser.parse_args()

    config = load_config(args.config)

    if args.list:
        print("Available computers:")
        for name, comp in config.items():
            mac = comp.get("mac", "N/A")
            broadcast = comp.get("broadcast", "255.255.255.255")
            port = comp.get("port", 9)
            print(f"- {name}: mac={mac}, broadcast={broadcast}, port={port}")
        sys.exit(0)

    if not args.name:
        parser.print_help()
        sys.exit(1)

    if args.name not in config:
        print(f"Computer '{args.name}' not found in config.")
        print("Available computers:", ", ".join(config.keys()))
        sys.exit(1)

    comp = config[args.name]
    mac = comp.get("mac")
    broadcast = comp.get("broadcast", "255.255.255.255")
    port = comp.get("port", 9)

    if not mac:
        print(f"Computer '{args.name}' is missing 'mac' in config.")
        sys.exit(1)

    send_magic_packet(mac, broadcast, port)


if __name__ == "__main__":
    main()
