import shutil
import sys

TOOLS = [
    "naabu",
    "httpx-toolkit",
    "gowitness",
    "nuclei"
]

def check_dependencies():
    print("[*] Checking dependencies...")
    missing = []

    for tool in TOOLS:
        if shutil.which(tool):
            print(f"[✓] {tool} found")
        else:
            print(f"[✗] {tool} missing")
            missing.append(tool)

    if missing:
        print("\nInstall missing tools before running.")
        sys.exit(1)
