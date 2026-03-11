import subprocess
import os


def run_web_scan(ports_file, project_dir):

    http_file = f"{project_dir}/http.txt"
    screenshots_dir = f"{project_dir}/screenshots"
    nuclei_file = f"{project_dir}/nuclei.txt"

    os.makedirs(screenshots_dir, exist_ok=True)

    print("\nRunning httpx-toolkit\n")

    httpx_cmd = [
        "httpx-toolkit",
        "-l", ports_file,
        "-silent",
        "-o", http_file
    ]

    subprocess.run(httpx_cmd)

    # If no HTTP services found
    if not os.path.exists(http_file) or os.path.getsize(http_file) == 0:
        print("No HTTP services discovered")
        return http_file, None

    print("\nRunning Gowitness screenshots\n")

    gowitness_cmd = [
        "gowitness",
        "scan",
        "file",
        "-f", http_file,
        "--threads", "20",
        "--write-db",
        "--screenshot-path", screenshots_dir
    ]

    subprocess.run(gowitness_cmd, cwd=project_dir)

    run_nuclei = input("\nRun Nuclei scan? (y/n): ").lower()

    if run_nuclei == "y":

        print("\nRunning Nuclei\n")

        nuclei_cmd = [
            "nuclei",
            "-l", http_file,
            "-o", nuclei_file
        ]

        subprocess.run(nuclei_cmd)

        return http_file, nuclei_file

    return http_file, None
