import subprocess
import os


def run_web_scan(http_file, project_dir):

    screenshots_dir = f"{project_dir}/screenshots"
    nuclei_file = f"{project_dir}/nuclei.txt"

    os.makedirs(screenshots_dir, exist_ok=True)

    print("\nRunning Gowitness screenshots\n")

    cmd = [
        "gowitness",
        "scan",
        "file",
        "-f", http_file,
        "--threads", "20",
        "--screenshot-path", screenshots_dir,
        "--write-db"
    ]

    subprocess.run(cmd)

    print("\nScreenshots completed.")

    # Ask user if nuclei should run
    choice = input("\nDo you want to run Nuclei vulnerability scan? (y/n): ").strip().lower()

    if choice != "y":

        print("\nSkipping Nuclei scan.")
        return

    print("\nRunning Nuclei scan\n")

    cmd = [
        "nuclei",
        "-l", http_file,
        "-o", nuclei_file,
        "-c", "50",
        "-rate-limit", "150"
    ]

    subprocess.run(cmd)

    print(f"\nNuclei results saved to {nuclei_file}")
