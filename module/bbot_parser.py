import re


def parse_bbot_table(file):

    print("\nParsing BBOT ASN table\n")

    subnets = []

    with open(file) as f:

        for line in f:

            match = re.search(r"\d+\.\d+\.\d+\.\d+\/\d+", line)

            if match:

                subnets.append(match.group())

    print(f"Found {len(subnets)} subnets")

    return subnets
