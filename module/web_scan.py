import subprocess
from pathlib import Path


def run_httpx(input_ports, output_json):

    output_json = Path(output_json)

    if output_json.exists() and output_json.stat().st_size > 0:
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
        str(output_json)
    ]

    subprocess.run(cmd)


def run_gowitness(url_file, output_dir):

    output_dir = Path(output_dir)

    db_path = output_dir / "gowitness.db"
    screenshot_dir = output_dir / "screenshots"

    screenshot_dir.mkdir(parents=True, exist_ok=True)

    if db_path.exists() and db_path.stat().st_size > 0:
        print("[✓] Reusing gowitness database")
        return

    print("[*] Running gowitness screenshot capture...")

    cmd = [
        "gowitness",
        "scan",
        "file",
        "-f",
        url_file,
        "--db-path",
        str(db_path),
        "--screenshot-path",
        str(screenshot_dir),
        "--threads",
        "4"
    ]

    subprocess.run(cmd)


def run_nuclei(url_file, output_file):

    print("[*] Running nuclei (stealth red-team mode)...")

    cmd = [
        "nuclei",
        "-l",
        url_file,

        # limited important templates
        "-tags",
        "cves,misconfig,exposure,tech",

        # severity filtering
        "-severity",
        "critical,high",

        # disable interactsh noise
        "-no-interactsh",

        # low noise settings
        "-rate-limit",
        "30",

        "-c",
        "5",

        "-retries",
        "1",

        "-timeout",
        "4",

        "-silent",

        "-o",
        output_file
    ]

    subprocess.run(cmd)
