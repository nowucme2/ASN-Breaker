import subprocess
from pathlib import Path


def run_httpx(input_ports, output_json):

    output_json = Path(output_json)

    print("[*] Running httpx scan...")

    cmd = [
        "httpx-toolkit",
        "-l",
        str(input_ports),
        "-title",
        "-tech-detect",
        "-status-code",
        "-server",
        "-silent",
        "-json"
    ]

    if output_json.exists():

        print("[*] Appending httpx results...")

        with open(output_json, "a") as f:
            subprocess.run(cmd, stdout=f)

    else:

        cmd.extend(["-o", str(output_json)])

        subprocess.run(cmd)


def run_gowitness(url_file, output_dir):

    output_dir = Path(output_dir)
    screenshot_dir = output_dir / "screenshots"

    screenshot_dir.mkdir(parents=True, exist_ok=True)

    print("[*] Running gowitness screenshot capture...")

    cmd = [
        "gowitness",
        "scan",
        "file",
        "-f",
        str(Path(url_file).resolve()),   # FIX: absolute path
        "--write-db",
        "--screenshot-path",
        str(screenshot_dir),
        "--threads",
        "4"
    ]

    subprocess.run(cmd, cwd=str(output_dir))


def run_nuclei(url_file, output_file):

    print("[*] Running nuclei (stealth red-team mode)...")

    cmd = [
        "nuclei",
        "-l",
        str(url_file),

        "-tags",
        "cves,misconfig,exposure,tech",

        "-severity",
        "critical,high",

        "-no-interactsh",

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
        str(output_file)
    ]

    subprocess.run(cmd)
