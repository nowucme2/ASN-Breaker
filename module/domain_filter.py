import subprocess
import os


def domain_filter(ip_file, project_dir):

    keyword = input("\nEnter domain keyword to match (example: sisainfosec): ").strip().lower()

    ptr_file = os.path.join(project_dir, "ptr_results.txt")
    filtered_file = os.path.join(project_dir, "filtered_ips.txt")

    print("\nRunning PTR lookup using dnsx...\n")

    cmd = [
        "dnsx",
        "-l", ip_file,
        "-ptr",
        "-silent",
        "-resp",
        "-o", ptr_file
    ]

    subprocess.run(cmd)

    print("\nFiltering results based on keyword...\n")

    valid_ips = []

    with open(ptr_file) as f:
        for line in f:

            if keyword in line.lower():

                ip = line.split()[0]
                valid_ips.append(ip)

    with open(filtered_file, "w") as f:
        for ip in valid_ips:
            f.write(ip + "\n")

    print(f"\nMatched {len(valid_ips)} IPs containing '{keyword}'")

    return filtered_file
