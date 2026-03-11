import subprocess
from pathlib import Path


def run_httpx(input_ports, output_json):

    if Path(output_json).exists() and Path(output_json).stat().st_size > 0:
        print("[✓] Reusing httpx results")
        return

    cmd = [
        "httpx-toolkit",
        "-l",
        input_ports,
        "-title",
        "-tech-detect",
        "-status-code",
        "-server",
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

    cmd = [
        "nuclei",
        "-l",
        url_file,
        "-severity",
        "critical,high,medium",
        "-o",
        output_file
    ]

    subprocess.run(cmd)
