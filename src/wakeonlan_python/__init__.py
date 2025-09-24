"""Wake-on-LAN utilities and CLI helpers."""

from __future__ import annotations

import re
import socket
import sys
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional

import psutil
import yaml

__all__ = [
    "send_magic_packet",
    "load_config",
    "list_interfaces",
    "looks_like_mac",
    "DEFAULT_CONFIG_PATH",
]

DEFAULT_CONFIG_PATH = Path.home() / ".wol.yaml"


def send_magic_packet(
    mac_address: str,
    broadcast: str = "255.255.255.255",
    port: int = 9,
    interface: Optional[str] = None,
) -> None:
    """Send a Wake-on-LAN magic packet."""
    mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
    if len(mac_bytes) != 6:
        raise ValueError(f"Invalid MAC address format: {mac_address}")

    packet = b"\xFF" * 6 + mac_bytes * 16

    for iface, addrs in psutil.net_if_addrs().items():
        if interface and iface != interface:
            continue
        for addr in addrs:
            if addr.family == socket.AF_INET:
                local_ip = addr.address
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        sock.bind((local_ip, 0))
                        sock.sendto(packet, (broadcast, port))
                    print(
                        f"Magic Packet sent to {mac_address} via {iface} ({local_ip}) -> "
                        f"{broadcast}:{port}"
                    )
                except Exception as exc:  # pragma: no cover - relies on network state
                    print(f"Failed to send from {local_ip} ({iface}): {exc}")


def load_config(path: str | Path) -> Mapping[str, Dict[str, object]]:
    """Load Wake-on-LAN configuration from a YAML file."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        defaults = dict(data.pop("@default", {}))

        for name, comp in list(data.items()):
            if isinstance(comp, str):
                comp = {"mac": comp}
            merged = defaults.copy()
            merged.update(comp)
            data[name] = merged

        return data
    except Exception as exc:  # pragma: no cover - relies on filesystem state
        print(f"Failed to load YAML file: {exc}")
        sys.exit(1)


def list_interfaces() -> None:
    """Print available network interfaces with their IPv4 addresses."""
    print("Available network interfaces:")
    for iface, addrs in psutil.net_if_addrs().items():
        ipv4_list: Iterable[str] = [addr.address for addr in addrs if addr.family == socket.AF_INET]
        if ipv4_list:
            print(f"  {iface}: {', '.join(ipv4_list)}")
        else:
            print(f"  {iface}: (no IPv4)")


def looks_like_mac(value: str) -> bool:
    """Return True if *value* matches a MAC address pattern."""
    return bool(re.fullmatch(r"([0-9A-Fa-f]{2}([-:])){5}[0-9A-Fa-f]{2}", value))
