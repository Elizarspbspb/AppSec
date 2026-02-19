import re
from models.finding import Finding

SINKS = [
    "innerHTML",
    "document.write",
    "eval(",
    "setTimeout(",
    "location.href"
]

SOURCES = [
    "location.search",
    "document.cookie",
    "localStorage",
    "postMessage"
]

def analyze(js_text):
    findings = []

    for sink in SINKS:
        if sink in js_text:
            findings.append(Finding(
                "DOM XSS",
                f"JS sink detected: {sink}",
                "Medium",
                "Potential XSS sink in JavaScript"
            ))

    for src in SOURCES:
        if src in js_text:
            findings.append(Finding(
                "DOM XSS",
                f"JS source detected: {src}",
                "Info",
                "User-controlled source"
            ))

    return findings