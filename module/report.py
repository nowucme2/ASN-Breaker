import os


def generate_report(subnets):

    ips=open("output/ips.txt").read()

    http=open("output/http.txt").read()

    nuclei=""

    if os.path.exists("output/nuclei.txt"):

        nuclei=open("output/nuclei.txt").read()

    rows=""

    for s in subnets:

        rows+=f"<tr><td>{s['subnet']}</td><td>{s['limit']}</td></tr>"

    html=f"""
<html>
<h1>ASN Breaker Report</h1>

<h2>Subnets</h2>

<table border=1>
<tr><th>Subnet</th><th>Limit</th></tr>
{rows}
</table>

<h2>Download IP List</h2>

<button onclick="download()">Download</button>

<script>
function download(){{
var text=`{ips}`;
var blob=new Blob([text]);
var link=document.createElement("a");
link.href=URL.createObjectURL(blob);
link.download="ips.txt";
link.click();
}}
</script>

<h2>HTTP Services</h2>
<pre>{http}</pre>

<h2>Nuclei Results</h2>
<pre>{nuclei}</pre>

</html>
"""

    open("output/report.html","w").write(html)
