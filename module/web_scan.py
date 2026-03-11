import subprocess
import os


def run_web_scan(http_file):

    screenshots="output/screenshots"

    subprocess.run(["gowitness","scan","file","-f",http_file,"-P",screenshots])

    nuclei_out="output/nuclei.txt"

    subprocess.run(["nuclei","-l",http_file,"-severity","critical,high,medium","-o",nuclei_out])
