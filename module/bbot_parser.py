import re

def parse_bbot_file(file_path):
    subnets = []

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            match = re.search(r'\d+\.\d+\.\d+\.\d+\/\d+', line)
            if match:
                subnets.append(match.group())

    return list(set(subnets))
