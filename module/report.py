def generate_report(subnets, project_dir):

    report = f"{project_dir}/report.html"

    with open(report, "w") as f:

        f.write("<html><body>")
        f.write("<h1>ASN Breaker Report</h1>")

        f.write("<h2>Subnets</h2><ul>")

        for s in subnets:

            f.write(f"<li>{s['subnet']}</li>")

        f.write("</ul></body></html>")

    print(f"\nReport generated: {report}")
