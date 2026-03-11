import shutil

tools = ["naabu", "httpx-toolkit", "gowitness", "nuclei"]


def check_dependencies():

    print("\nChecking dependencies\n")

    for tool in tools:

        if shutil.which(tool):

            print(f"{tool} OK")

        else:

            print(f"{tool} NOT FOUND")
