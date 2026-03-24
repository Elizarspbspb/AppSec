#go install github.com/lc/gau/v2/cmd/gau@latest
#go install github.com/tomnomnom/waybackurls@latest
#go install github.com/hakluke/hakrawler@latest
#go install github.com/ffuf/ffuf@latest

#git clone https://github.com/maurosoria/dirsearch.git
#git clone https://github.com/GerbenJavado/LinkFinder.git

import subprocess
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

TARGET = "http://62.173.140.174:36100"
WORDLIST = "/usr/share/wordlists/dirb/common.txt"

DIRSEARCH_PATH = "./dirsearch/dirsearch.py"
LINKFINDER_PATH = "./LinkFinder/linkfinder.py"

all_urls = set()
js_files = set()


# ------------------------
# Helper
# ------------------------
def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        #print("result.stdout.splitlines() = ", result.stdout.splitlines())
        return result.stdout.splitlines()
    except Exception as e:
        print("[ERROR]", e)
        return []


# ------------------------
# gau + waybackurls
# ------------------------
def collect_urls():
    print("[*] Running gau...")
    #gau = run_command(f"gau {TARGET}")
    gau = run_command("gau {}".format(TARGET))
    #print("[*] Running waybackurls...")
    #wayback = run_command(f"waybackurls {TARGET}")
    wayback = run_command("waybackurls {}".format(TARGET))

    return set(gau + wayback)


# ------------------------
# hakrawler
# ------------------------
def crawl():
    print("[*] Running hakrawler...")
    #return set(run_command(f"echo {TARGET} | hakrawler"))
    return set(run_command("echo {} | hakrawler".format(TARGET)))


# ------------------------
# ffuf
# ------------------------
def fuzz_ffuf():
    print("[*] Running ffuf...")
    #output = run_command(f"ffuf -u {TARGET}/FUZZ -w {WORDLIST} -mc 200 -fc 404 -of csv")
    output = run_command("ffuf -u {}/FUZZ -w {} -mc 200 -fc 404 -of csv".format(TARGET, WORDLIST))

    urls = set()
    for line in output:
        if TARGET in line:
            urls.add(line.split(",")[0])
    return urls


# ------------------------
# dirsearch
# ------------------------
def fuzz_dirsearch():
    print("[*] Running dirsearch...")
    #output = run_command(f"python3 dirsearch.py -u {TARGET} -w {WORDLIST} --plain-text-report=-")
    output = run_command("python3 {} -u {} -w {} --plain-text-report=-".format(DIRSEARCH_PATH, TARGET, WORDLIST))

    urls = set()
    for line in output:
        if TARGET in line:
            urls.add(line.strip())
    return urls


# ------------------------
# Extract JS
# ------------------------
def extract_js(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        for script in soup.find_all("script", src=True):
            js_url = urljoin(url, script["src"])
            js_files.add(js_url)

    except:
        pass


# ------------------------
# LinkFinder
# ------------------------
def run_linkfinder(js_url):
    #print(f"[JS] {js_url}")
    print("[JS] {}".format(js_url))
    #cmd = f"python3 linkfinder.py -i {js_url} -o cli"
    cmd = "python3 {} -i {} -o cli.format(LINKFINDER_PATH, js_url)"
    results = run_command(cmd)

    for r in results:
        print("   ", r)

def analyze_page(url):
    try:
        r = requests.get(url, timeout=5)
    except:
        return

    soup = BeautifulSoup(r.text, "html.parser")

    print("\n" + "="*60)
    print("URL:", url)

    # --- формы ---
    forms = soup.find_all("form")
    if forms:
        print(" Forms:")
        for form in forms:
            action = form.get("action")
            if not action:
                action = url
            else:
                action = urljoin(url, action)

            method = form.get("method", "GET").upper()
            print(f"  -> {method} {action}")

            for inp in form.find_all(["input", "textarea", "select"]):
                print("     ", {
                    "name": inp.get("name"),
                    "type": inp.get("type", "text")
                })
                
# ------------------------
# MAIN
# ------------------------
def main():
    global all_urls

    # 1. catch URL
    all_urls |= collect_urls()
    print(all_urls)
    all_urls |= crawl()
    print(all_urls)
    all_urls |= fuzz_ffuf()
    print(all_urls)
    all_urls |= fuzz_dirsearch()
    print(all_urls)

    print("\n[+] TOTAL URLS FOUND:", len(all_urls))

    # 2. check and catch JS
    for url in list(all_urls):
       if "FUZZ" in url:
            continue
       print("[URL]", url)
       analyze_page(url)
       extract_js(url)

    # 3. analyzing JS
    print("\n[+] JS FILES FOUND:", len(js_files))
    for js in js_files:
        run_linkfinder(js)


if __name__ == "__main__":
    main()