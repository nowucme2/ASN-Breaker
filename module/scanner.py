import ipaddress
import subprocess
import os


def generate_ips(subnets, project_dir):

    ip_file = f"{project_dir}/ips.txt"

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    print("\nGenerating IP list\n")

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


def run_scanner(subnets, project_dir, reuse=False):

    ip_file = generate_ips(subnets, project_dir)

    ports_file = run_naabu(ip_file, project_dir)

    return ports_file
