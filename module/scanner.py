import ipaddress
import subprocess
import os

OUTPUT="output"


def generate_ips(subnets):

    file=f"{OUTPUT}/ips.txt"

    with open(file,"w") as f:

        for s in subnets:

            network=ipaddress.IPv4Network(s["subnet"])

            count=0

            for ip in network.hosts():

                if count>=s["limit"]:
                    break

                f.write(str(ip)+"\n")

                count+=1

    return file


def run_scanner(subnets):

    ip_file=generate_ips(subnets)

    ports="output/ports.txt"

    subprocess.run(["naabu","-list",ip_file,"-top-ports","100","-o",ports])

    http="output/http.txt"

    subprocess.run(f"cat {ports} | httpx-toolkit -silent -o {http}",shell=True)

    return http
