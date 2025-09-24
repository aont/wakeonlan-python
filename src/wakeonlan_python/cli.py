"""Command line entry point for wakeonlan-python."""

from __future__ import annotations

import argparse
import sys

from . import (
    DEFAULT_CONFIG_PATH,
    list_interfaces,
    load_config,
    looks_like_mac,
    send_magic_packet,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Wake-on-LAN using YAML configuration, computer name, or direct MAC input",
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Target computer name defined in YAML, or MAC address",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        default=str(DEFAULT_CONFIG_PATH),
        help=f"YAML config file (default: {DEFAULT_CONFIG_PATH})",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List available computers from config",
    )
    parser.add_argument(
        "--list-interfaces",
        action="store_true",
        help="List available network interfaces and exit",
    )
    parser.add_argument(
        "-m",
        "--mac",
        help="Directly specify MAC address (e.g. 00:11:22:33:44:55)",
    )
    parser.add_argument(
        "-b",
        "--broadcast",
        default="255.255.255.255",
        help="Broadcast address (default: 255.255.255.255)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=9,
        help="UDP port (default: 9)",
    )
    parser.add_argument(
        "-i",
        "--interface",
        help="Network interface to use",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_interfaces:
        list_interfaces()
        sys.exit(0)

    if args.mac:
        send_magic_packet(args.mac, args.broadcast, args.port, args.interface)
        sys.exit(0)

    if args.name and looks_like_mac(args.name):
        send_magic_packet(args.name, args.broadcast, args.port, args.interface)
        sys.exit(0)

    config = load_config(args.config)

    if args.list:
        print("Available computers:")
        for name, comp in config.items():
            mac = comp.get("mac", "N/A")
            broadcast = comp.get("broadcast", "255.255.255.255")
            port = comp.get("port", 9)
            interface = comp.get("interface", "all")
            print(
                f"- {name}: mac={mac}, broadcast={broadcast}, port={port}, interface={interface}"
            )
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
    interface = comp.get("interface")

    if not mac:
        print(f"Computer '{args.name}' is missing 'mac' in config.")
        sys.exit(1)

    send_magic_packet(mac, broadcast, port, interface)


if __name__ == "__main__":  # pragma: no cover - convenience entrypoint
    main()
