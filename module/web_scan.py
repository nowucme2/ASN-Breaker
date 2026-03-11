import subprocess
import os


def run_web_scan(ports_file, project_dir):

    http_file = f"{project_dir}/http.txt"
    screenshots_dir = f"{project_dir}/screenshots"
    gowitness_db = f"{project_dir}/gowitness.sqlite3"
    nuclei_file = f"{project_dir}/nuclei.txt"

    os.makedirs(screenshots_dir, exist_ok=True)

    # -------------------------
    # Step 1: HTTP discovery
    # -------------------------

    print("\nRunning httpx-toolkit\n")

    cmd_httpx = [
        "httpx-toolkit",
        "-l", ports_file,
        "-silent",
        "-o", http_file
    ]

    subprocess.run(cmd_httpx)

    if not os.path.exists(http_file) or os.path.getsize(http_file) == 0:

        print("\nNo HTTP services found.\n")
        return http_file, None

    # -------------------------
    # Step 2: Screenshots
    # -------------------------

    print("\nRunning Gowitness screenshots\n")

    cmd_gowitness = [
        "gowitness",
        "scan",
        "file",
        "-f", http_file,
        "--write-db",
        "--db-path", gowitness_db,
        "--screenshot-path", screenshots_dir,
        "--threads", "20"
    ]

    subprocess.run(cmd_gowitness)

    # -------------------------
    # Step 3: Ask nuclei
    # -------------------------

    run_nuclei = input("\nRun Nuclei vulnerability scan? (y/n): ").strip().lower()

    if run_nuclei == "y":

        print("\nRunning Nuclei scan\n")

        cmd_nuclei = [
            "nuclei",
            "-l", http_file,
            "-o", nuclei_file
        ]

        subprocess.run(cmd_nuclei)

        return http_file, nuclei_file

    else:

        print("\nSkipping Nuclei scan\n")

        return http_file, None
