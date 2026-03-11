import requests


def get_asn_prefixes(asn):

    print(f"\nFetching prefixes for {asn}")

    url = f"https://api.bgpview.io/asn/{asn}/prefixes"

    data = requests.get(url).json()

    subnets = []

    for p in data["data"]["ipv4_prefixes"]:

        subnets.append(p["prefix"])

    print(f"Found {len(subnets)} prefixes")

    return subnets
