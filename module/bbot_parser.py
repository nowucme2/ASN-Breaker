import re


def parse_bbot_table(file):

    subnets = []

    with open(file) as f:

        for line in f:

            match = re.search(r"(\d+\.\d+\.\d+\.\d+/\d+)", line)

            if match:

                subnet = match.group(1)

                subnets.append({
                    "subnet": subnet,
                    "limit": 1000
                })

    print(f"Found {len(subnets)} subnets")

    return subnets
