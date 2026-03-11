import json
from pathlib import Path

def generate_html_report(httpx_json, report_file):

    rows = []

    with open(httpx_json) as f:
        for line in f:
            data = json.loads(line)

            url = data.get("url","")
            title = data.get("title","")
            status = data.get("status-code","")
            tech = ",".join(data.get("tech",[]))

            rows.append(f"""
            <tr>
            <td>{url}</td>
            <td>{status}</td>
            <td>{title}</td>
            <td>{tech}</td>
            </tr>
            """)

    html = f"""
    <html>
    <body>
    <h1>ASN Breaker Report</h1>
    <table border="1">
    <tr>
    <th>URL</th>
    <th>Status</th>
    <th>Title</th>
    <th>Technology</th>
    </tr>
    {''.join(rows)}
    </table>
    </body>
    </html>
    """

    with open(report_file,"w") as f:
        f.write(html)
