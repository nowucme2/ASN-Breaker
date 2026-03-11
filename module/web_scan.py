import subprocess
import os

OUTPUT_DIR = "output"


def run_gowitness(http_file):

    print("\nRunning Gowitness screenshots\n")

    os.makedirs(f"{OUTPUT_DIR}/screenshots", exist_ok=True)

    cmd = [
        "gowitness",
        "scan",
        "file",
        "-f", http_file,
        "--threads", "20",
        "--write-db"
    ]

    subprocess.run(cmd)


def run_nuclei(http_file):

    print("\nRunning Nuclei scan\n")

    nuclei_output = f"{OUTPUT_DIR}/nuclei.txt"

    cmd = [
        "nuclei",
        "-l", http_file,
        "-o", nuclei_output
    ]

    subprocess.run(cmd)

    print(f"Vulnerabilities saved to {nuclei_output}")


def run_web_scan(http_file):

    run_gowitness(http_file)

    run_nuclei(http_file)
