from pathlib import Path

def create_project(target):
    base = Path("output") / target

    dirs = [
        "ips",
        "naabu",
        "httpx",
        "gowitness",
        "nuclei",
        "reports"
    ]

    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)

    return base
