import ipaddress
import os
import subprocess


def generate_ips(subnets, project_dir):

    full_ip_file = f"{project_dir}/ips_full.txt"
    scan_ip_file = f"{project_dir}/ips_scan.txt"

    print("\nCalculating total IP count...\n")

    total_ips = 0

    for entry in subnets:

        subnet = entry["subnet"]
        network = ipaddress.IPv4Network(subnet)

        total_ips += network.num_addresses

    print(f"Total IPs discovered: {total_ips}\n")

    choice = input(
        "How many IPs do you want to scan?\n"
        "1) 100\n"
        "2) 500\n"
        "3) 1000\n"
        "4) Custom\n"
        "Select option: "
    )

    if choice == "1":
        scan_limit = 100
    elif choice == "2":
        scan_limit = 500
    elif choice == "3":
        scan_limit = 1000
    else:
        scan_limit = int(input("Enter custom number: "))

    print("\nGenerating IP list...\n")

    count = 0

    with open(full_ip_file, "w") as full_f, open(scan_ip_file, "w") as scan_f:

        for entry in subnets:

            subnet = entry["subnet"]
            network = ipaddress.IPv4Network(subnet)

            for ip in network.hosts():

                full_f.write(str(ip) + "\n")

                if count < scan_limit:
                    scan_f.write(str(ip) + "\n")
                    count += 1

    print(f"Full IP list saved to: {full_ip_file}")
    print(f"Scan IP list saved to: {scan_ip_file}\n")

    return scan_ip_file


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

    subprocess.run(cmd)

    return ports_file
