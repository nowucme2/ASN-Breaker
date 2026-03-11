import os


def init_project():

    project = input("Enter project name: ").strip()

    base = f"output/{project}"

    if os.path.exists(base):

        print("Project already exists.")

        print("1) Use existing scan data")
        print("2) Run new scan")
        print("3) Exit")

        choice = input("Select option: ")

        if choice == "1":

            return base, True

        elif choice == "2":

            return base, False

        else:

            exit()

    os.makedirs(base, exist_ok=True)

    return base, False
