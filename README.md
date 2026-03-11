<!-- =============================== -->

<!--           ASN BREAKER           -->

<!-- =============================== -->

<p align="center">
<img src="assests/Image Mar 11, 2026, 09_31_12 PM.png" width="450"/>
</p>

<h1 align="center">ASN Breaker</h1>

<p align="center">
Recon Automation Framework<br>
Created by <b>Abhishek CN</b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-red?style=for-the-badge\&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux-red?style=for-the-badge\&logo=linux)
![Security](https://img.shields.io/badge/RedTeam-Recon-red?style=for-the-badge\&logo=hackthebox)
![Status](https://img.shields.io/badge/Status-Active-red?style=for-the-badge)

</p>

---

# 🐺 ASN Breaker

**ASN Breaker** is a reconnaissance automation tool designed for **Red Team operations and internal penetration testing**.

It automates the workflow of:

* ASN parsing
* Subnet analysis
* IP sampling
* Port scanning
* Web service discovery
* Screenshot collection
* Vulnerability scanning
* HTML reporting

All scans run in **structured batches** allowing large targets to be scanned **safely and resumably**.

---

# ⚙ Recon Architecture

```
ASN / CIDR / BBOT Input
          │
          ▼
   Subnet Intelligence
          │
          ▼
     IP Sampling
          │
          ▼
     Batch Creation
          │
          ▼
   Naabu Port Scan
          │
          ▼
  HTTPX Web Discovery
          │
          ▼
 Gowitness Screenshots
          │
          ▼
 Optional Nuclei Scan
          │
          ▼
    HTML Recon Report
```

---

# 🚀 Features

✔ ASN parsing from **BBOT output**
✔ Manual **ASN / CIDR support**
✔ Smart **IP sampling for large ranges**
✔ **Batch-based scanning system**
✔ Resume scans automatically
✔ Automated **port scanning (Naabu)**
✔ Web discovery with **HTTPX**
✔ Screenshot capture using **Gowitness**
✔ Optional **low-noise Nuclei scanning**
✔ Structured **HTML recon reports**
✔ Full **scan logging system**

---

# 🧰 Tools Used

| Tool      | Purpose                        |
| --------- | ------------------------------ |
| Naabu     | Fast port scanning             |
| HTTPX     | Web detection & fingerprinting |
| Gowitness | Screenshot automation          |
| Nuclei    | Vulnerability scanning         |
| BBOT      | ASN data collection            |

---

# 📦 Installation

Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/asn-breaker.git
cd asn-breaker
```

Install Python dependencies

```bash
pip install -r requirements.txt
```

Install required recon tools

```bash
sudo apt install gowitness

go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
```

---

# ▶ Usage

Scan using BBOT ASN file

```bash
python3 asn_breaker.py --bbot asn_table.txt
```

Scan using manual CIDR

```bash
python3 asn_breaker.py --cidr 192.168.0.0/16
```

---

# 📁 Output Structure

```
output/
 └── TARGET
     ├── ips
     │   ├── master_ip_list.txt
     │   └── progress.json
     │
     ├── batches
     │   ├── batch_1
     │   ├── batch_2
     │   └── batch_3
     │
     ├── naabu
     ├── httpx
     ├── gowitness
     ├── nuclei
     ├── reports
     └── logs
```

---

# 🔄 Resume Capability

Scan progress automatically saved in:

```
output/TARGET/ips/progress.json
```

Example:

```json
{"last_index": 500}
```

Next run continues from **IP 501**.

---

# 📊 HTML Report

Final recon report generated at:

```
output/TARGET/reports/final_report.html
```

Includes:

* URLs discovered
* HTTP status codes
* Page titles
* Technologies detected
* Screenshot previews

---

# 🧾 Logging

Scan activity recorded in:

```
output/TARGET/logs/scan.log
```

Example entries:

```
Project started
Batch started
Naabu scan executed
HTTPX scan executed
Gowitness screenshots captured
Nuclei scan executed
Report generated
```

---

# 👤 Author

**Abhishek CN**

Red Team • Offensive Security • Recon Automation

---

# ⚠ Disclaimer

This tool is intended for **authorized security testing and research only**.
Do **not** use against systems without permission.

---
