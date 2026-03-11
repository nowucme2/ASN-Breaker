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
from module.domain_filter import domain_filter


def main():

    show_banner()

    check_dependencies()

    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--bbot", help="BBOT ASN table")
    parser.add_argument("-a", "--asn", help="ASN number")
    parser.add_argument("-c", "--cidr", help="CIDR subnet")

    args = parser.parse_args()

    project_dir, reuse = init_project()

    if args.bbot:

        raw_subnets = parse_bbot_table(args.bbot)

    elif args.asn:

        raw_subnets = get_asn_prefixes(args.asn)

    elif args.cidr:

        raw_subnets = [args.cidr]

    else:

        print("Provide -b OR -a OR -c")
        return

    subnets = analyze_subnets(raw_subnets)

    ip_file = run_scanner(subnets, project_dir, reuse)

    # NEW DOMAIN FILTER
    filtered_ips = domain_filter(ip_file, project_dir)

    http_file = run_web_scan(filtered_ips, project_dir)

    generate_report(subnets, project_dir)


if __name__ == "__main__":
    main()
