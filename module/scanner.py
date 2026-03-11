import ipaddress
import subprocess
import os
import random


def generate_ips(subnets, project_dir):

    ip_file = f"{project_dir}/ips.txt"

    all_ips = []

    for entry in subnets:

        network = ipaddress.IPv4Network(entry["subnet"])

        for ip in network.hosts():

            all_ips.append(str(ip))

    total = len(all_ips)

    print(f"\nTotal IPs discovered: {total}\n")

    print("1) 100")
    print("2) 500")
    print("3) 1000")
    print("4) Custom")
    print("5) Scan All")

    choice = input("Select option: ")

    if choice == "1":
        limit = 100
    elif choice == "2":
        limit = 500
    elif choice == "3":
        limit = 1000
    elif choice == "4":
        limit = int(input("Enter custom number: "))
    else:
        limit = total

    random.shuffle(all_ips)

    selected = all_ips[:limit]

    with open(ip_file, "w") as f:

        for ip in selected:

            f.write(ip + "\n")

    print(f"Saved {len(selected)} IPs for scanning")

    return ip_file


def run_naabu(ip_file, project_dir):

    ports_file = f"{project_dir}/ports.txt"

    cmd = [
        "naabu",
        "-list", ip_file,
        "-top-ports", "100",
        "-rate", "5000",
        "-o", ports_file
    ]

    subprocess.run(cmd)

    return ports_file


def run_scanner(subnets, project_dir, reuse=False):

    ports_file = f"{project_dir}/ports.txt"

    if reuse and os.path.exists(ports_file):

        print("Using existing Naabu results")

        return ports_file

    ip_file = generate_ips(subnets, project_dir)

    return run_naabu(ip_file, project_dir)
