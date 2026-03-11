import subprocess
from pathlib import Path


def run_httpx(input_ports, output_json):

    if Path(output_json).exists() and Path(output_json).stat().st_size > 0:
        print("[✓] Reusing httpx results")
        return

    print("[*] Running httpx scan...")

    cmd = [
        "httpx-toolkit",
        "-l",
        input_ports,
        "-title",
        "-tech-detect",
        "-status-code",
        "-server",
        "-silent",
        "-json",
        "-o",
        output_json
    ]

    subprocess.run(cmd)


def run_gowitness(url_file, output_dir):

    db = Path(output_dir) / "gowitness.db"

    if db.exists():
        print("[✓] Reusing gowitness db")
        return

    print("[*] Running gowitness screenshots...")

    cmd = [
        "gowitness",
        "scan",
        "file",
        "-f",
        url_file,
        "--write-db",
        str(db),
        "--screenshot-path",
        str(Path(output_dir) / "screenshots")
    ]

    subprocess.run(cmd)


def run_nuclei(url_file, output_file):

    print("[*] Running nuclei (stealth red-team mode)...")

    cmd = [
        "nuclei",
        "-l",
        url_file,

        # only important categories
        "-tags",
        "cves,misconfig,exposure,tech",

        # high impact only
        "-severity",
        "critical,high",

        # disable interactsh noise
        "-no-interactsh",

        # reduce traffic
        "-rate-limit",
        "30",

        # concurrency
        "-c",
        "5",

        # retries
        "-retries",
        "1",

        # timeout
        "-timeout",
        "4",

        "-silent",
        "-o",
        output_file
    ]

    subprocess.run(cmd)
