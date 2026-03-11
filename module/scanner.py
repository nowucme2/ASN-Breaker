import subprocess
from pathlib import Path

def run_naabu(ip_list, output_file):

    if Path(output_file).exists() and Path(output_file).stat().st_size > 0:
        print("[✓] Reusing existing naabu scan")
        return

    cmd = [
        "naabu",
        "-l",
        ip_list,
        "-p",
        "-",
        "-rate",
        "2000",
        "-o",
        output_file
    ]

    subprocess.run(cmd)
