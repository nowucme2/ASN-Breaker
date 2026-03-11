from pathlib import Path


def select_or_create_project():

    base = Path("output")
    base.mkdir(exist_ok=True)

    projects = [p.name for p in base.iterdir() if p.is_dir()]

    if projects:
        print("\nExisting Projects:\n")

        for i, p in enumerate(projects, 1):
            print(f"{i}. {p}")

        print(f"{len(projects)+1}. Create New Project")

        choice = input("\nSelect project number: ").strip()

        try:
            choice = int(choice)

            if choice <= len(projects):
                target = projects[choice-1]
                print(f"\n[✓] Using existing project: {target}")
            else:
                target = input("Enter new target name: ").strip()

        except:
            target = input("Enter new target name: ").strip()

    else:
        target = input("Enter new target name: ").strip()

    project_path = base / target

    dirs = [
        "ips",
        "naabu",
        "httpx",
        "gowitness",
        "nuclei",
        "reports"
    ]

    for d in dirs:
        (project_path / d).mkdir(parents=True, exist_ok=True)

    return target, project_path
