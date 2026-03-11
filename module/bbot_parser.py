import re

# CDN / Cloud providers to ignore
CDN_PROVIDERS = [
    "cloudflare",
    "akamai",
    "fastly",
    "cloudfront",
    "amazon",
    "aws",
    "google",
    "microsoft",
    "azure",
    "sendgrid",
]


def parse_bbot_table(file):

    print("\nParsing BBOT ASN table...\n")

    subnets = []
    seen = set()

    cdn_skipped = 0
    duplicate_skipped = 0

    with open(file) as f:

        for line in f:

            subnet_match = re.search(r"(\\d+\\.\\d+\\.\\d+\\.\\d+/\\d+)", line)

            if not subnet_match:
                continue

            subnet = subnet_match.group(1)

            line_lower = line.lower()

            # -----------------------------
            # CDN Filtering
            # -----------------------------

            if any(cdn in line_lower for cdn in CDN_PROVIDERS):

                print(f"Skipping CDN network: {subnet}")

                cdn_skipped += 1
                continue

            # -----------------------------
            # Duplicate Filtering
            # -----------------------------

            if subnet in seen:

                duplicate_skipped += 1
                continue

            seen.add(subnet)

            subnets.append({
                "subnet": subnet,
                "limit": 1000
            })

    print("\nSummary\n")

    print(f"Valid subnets: {len(subnets)}")
    print(f"CDN networks removed: {cdn_skipped}")
    print(f"Duplicate subnets removed: {duplicate_skipped}")

    return subnets
