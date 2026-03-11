import argparse

from module.banner import show_banner
from module.dependency_check import check_dependencies
from module.bbot_parser import parse_bbot_table
from module.subnet_intel import analyze_subnets
from module.asn_lookup import get_asn_prefixes
from module.scanner import run_scanner
from module.web_scan import run_web_scan
from module.report import generate_report


def main():

    show_banner()

    check_dependencies()

    parser = argparse.ArgumentParser(description="ASN Breaker")

    parser.add_argument("-b", "--bbot", help="BBOT ASN table file")
    parser.add_argument("-a", "--asn", help="ASN number")
    parser.add_argument("-c", "--cidr", help="CIDR subnet")

    args = parser.parse_args()

    raw_subnets = []

    if args.bbot:

        raw_subnets = parse_bbot_table(args.bbot)

    elif args.asn:

        raw_subnets = get_asn_prefixes(args.asn)

    elif args.cidr:

        raw_subnets = [args.cidr]

    else:

        print("Provide -b BBOT table OR -a ASN OR -c CIDR")
        return

    subnets = analyze_subnets(raw_subnets)

    http_file = run_scanner(subnets)

    run_web_scan(http_file)

    generate_report(subnets)

    print("\nScan finished. Open output/report.html")


if __name__ == "__main__":
    main()
