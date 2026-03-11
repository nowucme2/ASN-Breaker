#!/usr/bin/env python3

import argparse

from module.banner import show_banner
from module.dependency_check import check_dependencies
from module.bbot_parser import parse_bbot_table
from module.subnet_intel import analyze_subnets
from module.asn_lookup import get_asn_prefixes
from module.project import init_project
from module.scanner import run_scanner
from module.web_scan import run_web_scan
from module.report import generate_report


def main():

    show_banner()

    check_dependencies()

    parser = argparse.ArgumentParser(
        description="ASN Breaker - External Attack Surface Scanner"
    )

    parser.add_argument("-b", "--bbot", help="Input BBOT ASN table")
    parser.add_argument("-a", "--asn", help="Scan ASN directly")
    parser.add_argument("-c", "--cidr", help="Scan specific CIDR")

    args = parser.parse_args()

    project_dir, reuse = init_project()

    if args.bbot:

        print("\nParsing BBOT ASN table\n")
        raw_subnets = parse_bbot_table(args.bbot)

    elif args.asn:

        print("\nFetching ASN prefixes\n")
        raw_subnets = get_asn_prefixes(args.asn)

    elif args.cidr:

        raw_subnets = [{"subnet": args.cidr, "limit": 1000}]

    else:

        print("Please provide -b OR -a OR -c")
        return

    subnets = analyze_subnets(raw_subnets)

    ports_file = run_scanner(subnets, project_dir, reuse)

    http_file, nuclei_file = run_web_scan(ports_file, project_dir)

    generate_report(subnets, project_dir)

    print("\nScan Completed\n")


if __name__ == "__main__":
    main()
