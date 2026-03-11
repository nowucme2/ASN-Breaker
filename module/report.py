import json
from pathlib import Path


def generate_html_report(httpx_json, report_file):

    rows = []

    screenshot_dir = Path(report_file).parent.parent / "gowitness" / "screenshots"

    with open(httpx_json) as f:
        for line in f:

            data = json.loads(line)

            url = data.get("url","")
            title = data.get("title","")
            status = data.get("status-code","")

            tech = data.get("tech",[])
            tech = ",".join(tech)

            screenshot_name = url.replace("://","-").replace(":","-") + ".jpeg"
            screenshot_path = screenshot_dir / screenshot_name

            screenshot_html = ""

            if screenshot_path.exists():

                screenshot_html = f'<img src="../gowitness/screenshots/{screenshot_name}" width="300">'

            rows.append(f"""
            <tr>
            <td>{url}</td>
            <td>{status}</td>
            <td>{title}</td>
            <td>{tech}</td>
            <td>{screenshot_html}</td>
            </tr>
            """)

    html = f"""
    <html>
    <head>
    <title>ASN Breaker Report</title>
    <style>
    body {{font-family: Arial;}}
    table {{border-collapse: collapse; width: 100%;}}
    th, td {{border: 1px solid #ccc; padding: 8px;}}
    th {{background: #333; color: white;}}
    </style>
    </head>

    <body>

    <h1>ASN Breaker Recon Report</h1>

    <table>

    <tr>
    <th>URL</th>
    <th>Status</th>
    <th>Title</th>
    <th>Technology</th>
    <th>Screenshot</th>
    </tr>

    {''.join(rows)}

    </table>

    </body>
    </html>
    """

    with open(report_file,"w") as f:
        f.write(html)
