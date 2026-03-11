import subprocess


def run_web_scan(http_file, project_dir):

    print("\nRunning Gowitness\n")

    cmd = [
        "gowitness",
        "scan",
        "file",
        "-f", http_file,
        "--screenshot-path", f"{project_dir}/screenshots",
        "--threads", "20"
    ]

    subprocess.run(cmd)

    print("\nRunning Nuclei\n")

    nuclei_file = f"{project_dir}/nuclei.txt"

    cmd = [
        "nuclei",
        "-l", http_file,
        "-o", nuclei_file
    ]

    subprocess.run(cmd)

    print(f"Vulnerabilities saved to {nuclei_file}")
