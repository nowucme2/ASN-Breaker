import ipaddress


def analyze_subnets(raw):

    result = []

    for entry in raw:

        subnet = entry["subnet"]
        limit = entry["limit"]

        network = ipaddress.IPv4Network(subnet)

        size = network.num_addresses

        print(f"{subnet} | {size} IPs")

        result.append({
            "subnet": subnet,
            "limit": limit
        })

    return result
