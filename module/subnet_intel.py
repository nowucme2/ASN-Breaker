import ipaddress

CDN_KEYWORDS = [
"cloudflare",
"akamai",
"fastly",
"amazon",
"aws",
"google",
"microsoft",
"azure"
]

stats = {
"total":0,
"cdn":0,
"accepted":0,
"limited":0,
"skipped":0
}


def analyze_subnets(subnets):

    final = []

    stats["total"] = len(subnets)

    for subnet in subnets:

        network = ipaddress.IPv4Network(subnet)

        ip_count = network.num_addresses

        print(f"\n{subnet} | {ip_count} IPs")

        if ip_count <= 1000:

            stats["accepted"] += 1

            final.append({"subnet":subnet,"limit":ip_count})

        elif ip_count <= 50000:

            choice = input("Medium subnet continue? y/n: ")

            if choice.lower()=="y":

                stats["accepted"]+=1

                final.append({"subnet":subnet,"limit":ip_count})

            else:

                stats["skipped"]+=1

        else:

            print("Large subnet limiting to 1000")

            stats["limited"]+=1

            final.append({"subnet":subnet,"limit":1000})

    print_summary()

    return final


def print_summary():

    print("\n--- Scan Summary ---\n")

    print(f"Total Subnets : {stats['total']}")
    print(f"Accepted      : {stats['accepted']}")
    print(f"Limited       : {stats['limited']}")
    print(f"Skipped       : {stats['skipped']}")
