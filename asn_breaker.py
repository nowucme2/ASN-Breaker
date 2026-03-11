import argparse
from modules.subnet_parser import process_subnets
from modules.scanner import run_scanner
from modules.web_vuln_scan import run_web_scan
from modules.asn_lookup import get_asn_prefixes
from modules.report_generator import generate_report


def main():

    parser = argparse.ArgumentParser(description="ASN Breaker")

    parser.add_argument("-f", "--file", help="BBOT ASN table file")
    parser.add_argument("-a", "--asn", help="ASN number")
    parser.add_argument("-c", "--cidr", help="CIDR subnet")

    args = parser.parse_args()

    subnets = []

    if args.file:

        subnets = process_subnets(args.file)

    elif args.cidr:

        subnets = [{"subnet": args.cidr, "limit": 1000}]

    elif args.asn:

        prefixes = get_asn_prefixes(args.asn)

        for p in prefixes:

            subnets.append({"subnet": p, "limit": 1000})

    else:

        print("Provide -f OR -a OR -c")
        return

    http_file = run_scanner(subnets)

    run_web_scan(http_file)

    generate_report(subnets)

    print("\nASN Breaker scan complete")


if __name__ == "__main__":
    main()
