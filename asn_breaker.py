import argparse

from modules.banner import show_banner
from modules.dependency_check import check_dependencies
from modules.bbot_parser import parse_bbot_table
from modules.subnet_intel import analyze_subnets
from modules.asn_lookup import get_asn_prefixes
from modules.scanner import run_scanner
from modules.web_scan import run_web_scan
from modules.report import generate_report
from modules.project import init_project


def main():

    show_banner()

    check_dependencies()

    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--bbot", help="BBOT ASN table file")
    parser.add_argument("-a", "--asn", help="ASN number")
    parser.add_argument("-c", "--cidr", help="CIDR subnet")

    args = parser.parse_args()

    project_dir = init_project()

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

    http_file = run_scanner(subnets, project_dir)

    run_web_scan(http_file, project_dir)

    generate_report(subnets, project_dir)


if __name__ == "__main__":
    main()
