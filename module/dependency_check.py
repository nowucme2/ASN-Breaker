import shutil
import sys


TOOLS = ["naabu", "httpx-toolkit", "gowitness", "nuclei"]


def check_dependencies():

    print("\nChecking dependencies\n")

    for tool in TOOLS:

        if shutil.which(tool) is None:

            print(f"{tool} not installed")

            sys.exit()

        else:

            print(f"{tool} OK")
