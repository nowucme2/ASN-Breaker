import subprocess
import os
from pathlib import Path


def run_naabu(ip_list, output_file):

    output_path = Path(output_file)

    if output_path.exists() and output_path.stat().st_size > 0:
        print("[✓] Reusing existing naabu scan")
        return

    print("[*] Preparing Naabu scan (top 1000 ports)...")

    cmd = [
        "naabu",
        "-l",
        ip_list,
        "-top-ports",
        "1000",
        "-rate",
        "2000",
        "-o",
        output_file
    ]

    # Check if running as root
    if os.geteuid() != 0:
        ans = input("[!] Naabu SYN scan requires root privileges. Run with sudo? (y/n): ").strip().lower()
        if ans == "y":
            cmd.insert(0, "sudo")
        else:
            print("[*] Running without root (CONNECT scan - slower)")

    print("[*] Running Naabu...")
    subprocess.run(cmd)
