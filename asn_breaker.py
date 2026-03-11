import argparse
import json
from pathlib import Path

from module.banner import show_banner
from module.dependency_check import check_dependencies
from module.project import select_or_create_project
from module.bbot_parser import parse_bbot_file
from module.subnet_intel import clean_subnets, sample_ips
from module.scanner import run_naabu
from module.web_scan import run_httpx, run_gowitness, run_nuclei
from module.report import generate_html_report


def load_progress(progress_file):

    if progress_file.exists():
        with open(progress_file) as f:
            return json.load(f)

    return {"last_index": 0}


def save_progress(progress_file, index):

    with open(progress_file, "w") as f:
        json.dump({"last_index": index}, f)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--bbot", help="BBOT ASN table file")
    parser.add_argument("--cidr", help="Manual CIDR")

    args = parser.parse_args()

    show_banner()

    check_dependencies()

    target, project = select_or_create_project()

    ips_dir = project / "ips"
    ips_dir.mkdir(exist_ok=True)

    master_ip_file = ips_dir / "master_ip_list.txt"
    progress_file = ips_dir / "progress.json"

    # generate IP list only once
    if not master_ip_file.exists():

        subnets = []

        if args.bbot:
            subnets.extend(parse_bbot_file(args.bbot))

        if args.cidr:
            subnets.append(args.cidr)

        networks = clean_subnets(subnets)

        ips = sample_ips(networks)

        print(f"\nTotal IPs discovered: {len(ips)}")

        with open(master_ip_file, "w") as f:
            for ip in ips:
                f.write(ip + "\n")

    else:

        print("[✓] Reusing existing master IP list")

        with open(master_ip_file) as f:
            ips = [x.strip() for x in f.readlines()]

    progress = load_progress(progress_file)

    start_index = progress["last_index"]

    if start_index > 0:

        ans = input(f"\nPrevious scan stopped at IP {start_index}. Resume? (y/n): ")

        if ans.lower() != "y":
            start_index = 0

    count = int(input("How many IPs to scan now: "))

    selected_ips = ips[start_index:start_index + count]

    batch_id = (start_index // count) + 1

    batch_dir = project / "batches" / f"batch_{batch_id}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    ip_file = batch_dir / "ip_list.txt"

    with open(ip_file, "w") as f:
        for ip in selected_ips:
            f.write(ip + "\n")

    new_index = start_index + len(selected_ips)

    save_progress(progress_file, new_index)

    print(f"\nScanning IP range {start_index} → {new_index}")

    naabu_out = project / "naabu" / "ports.txt"
    naabu_out.parent.mkdir(exist_ok=True)

    run_naabu(str(ip_file), str(naabu_out))

    httpx_out = project / "httpx" / "httpx.json"
    httpx_out.parent.mkdir(exist_ok=True)

    run_httpx(str(naabu_out), str(httpx_out))

    urls = project / "httpx" / "urls.txt"

    with open(httpx_out) as f, open(urls, "w") as out:
        for line in f:
            data = json.loads(line)
            if "url" in data:
                out.write(data["url"] + "\n")

    gowitness_dir = project / "gowitness"

    run_gowitness(str(urls), str(gowitness_dir))

    run_nuclei_scan = input("\nRun Nuclei scan? (y/n): ").strip().lower()

    if run_nuclei_scan == "y":

        nuclei_output = project / "nuclei" / "nuclei.txt"
        nuclei_output.parent.mkdir(exist_ok=True)

        run_nuclei(str(urls), str(nuclei_output))

    report_file = project / "reports" / "final_report.html"
    report_file.parent.mkdir(exist_ok=True)

    generate_html_report(str(httpx_out), str(report_file))

    print(f"\n[✓] Report generated: {report_file}")


if __name__ == "__main__":
    main()
