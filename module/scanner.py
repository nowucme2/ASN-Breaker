import ipaddress
import subprocess
import os


def generate_ips(subnets, project_dir):

    ip_file = f"{project_dir}/ips.txt"

    if os.path.exists(ip_file):

        print("\nExisting IP list detected. Using old file.")
        return ip_file

    print("\nGenerating IP list")

    with open(ip_file, "w") as f:

        for entry in subnets:

            subnet = entry["subnet"]
            limit = entry["limit"]

            network = ipaddress.IPv4Network(subnet)

            count = 0

            for ip in network.hosts():

                if count >= limit:
                    break

                f.write(str(ip) + "\n")

                count += 1

    return ip_file


def run_naabu(ip_file, project_dir, reuse):

    ports_file = f"{project_dir}/ports.txt"

    if reuse and os.path.exists(ports_file):

        print("\nUsing existing Naabu results.")
        return ports_file

    print("\nRunning Naabu scan")

    cmd = [
        "naabu",
        "-list", ip_file,
        "-top-ports", "100",
        "-rate", "5000",
        "-o", ports_file
    ]

    subprocess.run(cmd)

    return ports_file


def run_scanner(subnets, project_dir, reuse):

    ip_file = generate_ips(subnets, project_dir)

    run_naabu(ip_file, project_dir, reuse)

    return ip_file
