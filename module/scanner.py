import subprocess
from pathlib import Path
import os


def run_naabu(ip_list, output_file):

    output_file = Path(output_file)

    print("[*] Running naabu scan...")

    cmd = [
        "naabu",
        "-l",
        ip_list,
        "-top-ports",
        "1000",
        "-rate",
        "2000"
    ]

    # check root privilege
    if os.geteuid() != 0:
        ans = input("[!] Naabu SYN scan needs root. Run with sudo? (y/n): ").strip().lower()
        if ans == "y":
            cmd.insert(0, "sudo")

    # append results instead of skipping
    if output_file.exists():

        print("[*] Appending new naabu results...")

        with open(output_file, "a") as f:
            subprocess.run(cmd, stdout=f)

    else:

        print("[*] Running initial naabu scan...")

        cmd.extend(["-o", str(output_file)])

        subprocess.run(cmd)
