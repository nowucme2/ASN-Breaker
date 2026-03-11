import os


def init_project():

    name = input("\nEnter project name: ").strip()

    project_dir = f"output/{name}"

    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(f"{project_dir}/screenshots", exist_ok=True)

    print(f"\nProject directory: {project_dir}")

    return project_dir
