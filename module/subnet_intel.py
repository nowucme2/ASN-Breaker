import ipaddress
import random

CDN_KEYWORDS = [
    "cloudflare",
    "akamai",
    "fastly"
]

def clean_subnets(subnets):
    valid = []

    for s in subnets:
        try:
            net = ipaddress.ip_network(s, strict=False)

            if net.version == 6:
                continue

            if str(net.network_address) == "0.0.0.0":
                continue

            valid.append(net)

        except:
            pass

    collapsed = list(ipaddress.collapse_addresses(valid))
    return collapsed


def sample_ips(networks):

    final_ips = []

    for net in networks:

        size = net.num_addresses

        if size < 2000:
            for ip in net.hosts():
                final_ips.append(str(ip))
        else:
            sample_size = 500
            for _ in range(sample_size):
                offset = random.randint(1, size-2)
                ip = net.network_address + offset
                final_ips.append(str(ip))

    return list(set(final_ips))
