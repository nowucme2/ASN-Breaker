import subprocess
import re


def get_asn_prefixes(asn):

    print(f"\nFetching prefixes for ASN {asn}\n")

    try:

        result = subprocess.run(
            ["whois", f"AS{asn}"],
            capture_output=True,
            text=True
        )

        output = result.stdout

    except Exception as e:

        print("ASN lookup failed:", e)
        return []

    prefixes = set()

    for line in output.splitlines():

        match = re.search(r"(\\d+\\.\\d+\\.\\d+\\.\\d+/\\d+)", line)

        if match:

            prefixes.add(match.group(1))

    subnets = []

    for subnet in prefixes:

        subnets.append({
            "subnet": subnet,
            "limit": 1000
        })

    print(f"Found {len(subnets)} prefixes from ASN\n")

    return subnets
