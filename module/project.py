import os
import sys


def init_project():

    name = input("\nEnter project name: ").strip()

    project_dir = f"output/{name}"

    if os.path.exists(project_dir):

        print("\nProject already exists.")

        print("1) Use existing scan data")
        print("2) Run new scan")
        print("3) Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            return project_dir, True

        elif choice == "2":
            return project_dir, False

        else:
            sys.exit()

    os.makedirs(project_dir)
    os.makedirs(f"{project_dir}/screenshots")

    return project_dir, False
