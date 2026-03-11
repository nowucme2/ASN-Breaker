import ipaddress
import subprocess
import os
import random
import sys


def calculate_total_ips(subnets):

    total = 0

    for entry in subnets:

        subnet = entry["subnet"]

        network = ipaddress.IPv4Network(subnet)

        total += network.num_addresses

    return total


def ask_scan_limit(total_ips):

    print(f"\nTotal IPs discovered from ASN: {total_ips}\n")

    print("How many IPs do you want to scan?")
    print("1) 100")
    print("2) 500")
    print("3) 1000")
    print("4) Custom")

    choice = input("\nSelect option: ")

    if choice == "1":
        return 100
    elif choice == "2":
        return 500
    elif choice == "3":
        return 1000
    elif choice == "4":
        return int(input("Enter number of IPs to scan: "))
    else:
        print("Invalid option, defaulting to 500")
        return 500


def generate_ips(subnets, project_dir):

    ip_file = f"{project_dir}/ips.txt"

    print("\nGenerating IP list...\n")

    all_ips = []

    for entry in subnets:

        subnet = entry["subnet"]
        limit = entry["limit"]

        network = ipaddress.IPv4Network(subnet)

        count = 0

        for ip in network.hosts():

            if count >= limit:
                break

            all_ips.append(str(ip))
            count += 1

    total_ips = len(all_ips)

    scan_limit = ask_scan_limit(total_ips)

    random.shuffle(all_ips)

    selected_ips = all_ips[:scan_limit]

    os.makedirs(project_dir, exist_ok=True)

    with open(ip_file, "w") as f:

        for ip in selected_ips:
            f.write(ip + "\n")

    print(f"\nSaved {scan_limit} IPs for scanning\n")

    return ip_file


def run_naabu(ip_file, project_dir):

    ports_file = f"{project_dir}/ports.txt"

    print("\nRunning Naabu scan\n")

    cmd = [
        "naabu",
        "-list", ip_file,
        "-top-ports", "100",
        "-rate", "5000",
        "-o", ports_file
    ]

    try:

        subprocess.run(cmd)

    except KeyboardInterrupt:

        print("\nScan interrupted by user")
        sys.exit(0)

    return ports_file


def run_scanner(subnets, project_dir, reuse=False):

    ports_file = f"{project_dir}/ports.txt"

    # -------------------------
    # Reuse existing scan
    # -------------------------

    if reuse and os.path.exists(ports_file):

        print("\nUsing existing Naabu scan results\n")

        return ports_file

    # -------------------------
    # Run fresh scan
    # -------------------------

    ip_file = generate_ips(subnets, project_dir)

    ports_file = run_naabu(ip_file, project_dir)

    return ports_file
