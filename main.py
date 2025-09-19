#!/usr/bin/env python3
import socket
import argparse
import yaml
import sys
import re
from pathlib import Path
import psutil


# --- Wake-on-LAN パケット送信 ---
def send_magic_packet(mac_address, broadcast="255.255.255.255", port=9, interface=None):
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
                    print(f"Magic Packet sent to {mac_address} via {iface} ({local_ip}) -> {broadcast}:{port}")
                except Exception as e:
                    print(f"Failed to send from {local_ip} ({iface}): {e}")


# --- YAML 読み込み ---
def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        defaults = data.pop("@default", {})

        # 各エントリを処理
        for name, comp in list(data.items()):
            # 値が文字列の場合（例: machine: "00:11:22:33:44:55"）
            if isinstance(comp, str):
                comp = {"mac": comp}
            # デフォルトをマージ
            merged = defaults.copy()
            merged.update(comp)
            data[name] = merged

        return data
    except Exception as e:
        print(f"Failed to load YAML file: {e}")
        sys.exit(1)


# --- インターフェース一覧 ---
def list_interfaces():
    print("Available network interfaces:")
    for iface, addrs in psutil.net_if_addrs().items():
        ipv4_list = [addr.address for addr in addrs if addr.family == socket.AF_INET]
        if ipv4_list:
            print(f"  {iface}: {', '.join(ipv4_list)}")
        else:
            print(f"  {iface}: (no IPv4)")


# --- MAC形式判定 ---
def looks_like_mac(s: str) -> bool:
    return bool(re.fullmatch(r"([0-9A-Fa-f]{2}([-:])){5}[0-9A-Fa-f]{2}", s))


# --- メイン処理 ---
def main():
    default_config = Path.home() / ".wol.yaml"

    parser = argparse.ArgumentParser(
        description="Wake-on-LAN using YAML configuration, computer name, or direct MAC input"
    )
    parser.add_argument("name", nargs="?", help="Target computer name defined in YAML, or MAC address")
    parser.add_argument(
        "-c", "--config", dest="config", default=str(default_config),
        help=f"YAML config file (default: {default_config})"
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="List available computers from config"
    )
    parser.add_argument(
        "--list-interfaces", action="store_true",
        help="List available network interfaces and exit"
    )

    # 短縮オプション追加
    parser.add_argument("-m", "--mac", help="Directly specify MAC address (e.g. 00:11:22:33:44:55)")
    parser.add_argument("-b", "--broadcast", default="255.255.255.255", help="Broadcast address (default: 255.255.255.255)")
    parser.add_argument("-p", "--port", type=int, default=9, help="UDP port (default: 9)")
    parser.add_argument("-i", "--interface", help="Network interface to use")

    args = parser.parse_args()

    if args.list_interfaces:
        list_interfaces()
        sys.exit(0)

    # 単発モード
    if args.mac:
        send_magic_packet(args.mac, args.broadcast, args.port, args.interface)
        sys.exit(0)

    # name が MAC アドレス形式の場合
    if args.name and looks_like_mac(args.name):
        send_magic_packet(args.name, args.broadcast, args.port, args.interface)
        sys.exit(0)

    # YAML 設定モード
    config = load_config(args.config)

    if args.list:
        print("Available computers:")
        for name, comp in config.items():
            mac = comp.get("mac", "N/A")
            broadcast = comp.get("broadcast", "255.255.255.255")
            port = comp.get("port", 9)
            iface = comp.get("interface", "all")
            print(f"- {name}: mac={mac}, broadcast={broadcast}, port={port}, interface={iface}")
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
    interface = comp.get("interface", None)

    if not mac:
        print(f"Computer '{args.name}' is missing 'mac' in config.")
        sys.exit(1)

    send_magic_packet(mac, broadcast, port, interface)


if __name__ == "__main__":
    main()
