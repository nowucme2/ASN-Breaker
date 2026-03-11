import ipaddress
import subprocess
import os


def generate_ips(subnets, project_dir):

    ip_file = f"{project_dir}/ips.txt"

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

    print(f"IPs saved to {ip_file}")

    return ip_file


def run_naabu(ip_file, project_dir):

    ports_file = f"{project_dir}/ports.txt"

    nmap_file = f"{project_dir}/nmap.xml"

    if os.path.exists(nmap_file):

        print("\nExisting Nmap scan detected. Skipping Naabu.\n")

        return ports_file

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


def run_httpx(ports_file, project_dir):

    http_file = f"{project_dir}/http.txt"

    print("\nRunning httpx-toolkit\n")

    cmd = f"cat {ports_file} | httpx-toolkit -silent -o {http_file}"

    subprocess.run(cmd, shell=True)

    print(f"HTTP services saved to {http_file}")

    return http_file


def run_scanner(subnets, project_dir):

    ip_file = generate_ips(subnets, project_dir)

    ports_file = run_naabu(ip_file, project_dir)

    http_file = run_httpx(ports_file, project_dir)

    return http_file
