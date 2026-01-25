import re
from models.finding import Finding

API_REGEX = [
    r"/api/[a-zA-Z0-9/_-]+",
    r"/v[0-9]+/[a-zA-Z0-9/_-]+",
    r"/graphql"
]

def analyze(text):
    findings = []
    seen = set()

    for rx in API_REGEX:
        for m in re.findall(rx, text):
            if m not in seen:
                seen.add(m)
                findings.append(Finding(
                    "API Surface",
                    "API endpoint discovered",
                    "Info",
                    m
                ))

    return findings