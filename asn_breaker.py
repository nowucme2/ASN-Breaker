import argparse
from pathlib import Path

from module.banner import show_banner
from module.dependency_check import check_dependencies
from module.project import create_project
from module.bbot_parser import parse_bbot_file
from module.subnet_intel import clean_subnets, sample_ips
from module.scanner import run_naabu
from module.web_scan import run_httpx, run_gowitness, run_nuclei
from module.report import generate_html_report


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--bbot", help="BBOT ASN table file")
    parser.add_argument("--asn", help="Manual ASN")
    parser.add_argument("--cidr", help="Manual CIDR")

    args = parser.parse_args()

    show_banner()
    check_dependencies()

    target = input("Enter Target Name: ").strip()

    project = create_project(target)

    subnets = []

    if args.bbot:
        subnets.extend(parse_bbot_file(args.bbot))

    if args.cidr:
        subnets.append(args.cidr)

    networks = clean_subnets(subnets)

    ips = sample_ips(networks)

    ip_file = project / "ips/ip_list.txt"

    with open(ip_file,"w") as f:
        for ip in ips:
            f.write(ip+"\n")

    print(f"[+] Generated {len(ips)} IPs")

    mode = input("Scan all IPs? (y/n): ")

    if mode.lower() != "y":
        n = int(input("Enter number of IPs: "))
        ips = ips[:n]

        with open(ip_file,"w") as f:
            for ip in ips:
                f.write(ip+"\n")

    naabu_out = project / "naabu/ports.txt"

    run_naabu(str(ip_file), str(naabu_out))

    httpx_out = project / "httpx/httpx.json"

    run_httpx(str(naabu_out), str(httpx_out))

    urls = project / "httpx/urls.txt"

    with open(httpx_out) as f, open(urls,"w") as out:
        for line in f:
            import json
            data = json.loads(line)
            if "url" in data:
                out.write(data["url"]+"\n")

    gowitness_dir = project / "gowitness"

    run_gowitness(str(urls), str(gowitness_dir))

    run_nuclei(str(urls), str(project / "nuclei/nuclei.txt"))

    report_file = project / "reports/final_report.html"

    generate_html_report(str(httpx_out), str(report_file))

    print(f"[✓] Report generated: {report_file}")


if __name__ == "__main__":
    main()
