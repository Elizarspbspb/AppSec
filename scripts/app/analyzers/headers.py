from models.finding import Finding

SEC_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy"
]

def analyze(headers):
    findings = []

    for h in SEC_HEADERS:
        if h not in headers:
            findings.append(Finding(
                "HTTP Headers",
                f"Missing security header: {h}",
                "Medium",
                f"{h} is not set"
            ))

    if headers.get("Access-Control-Allow-Origin") == "*":
        findings.append(Finding(
            "CORS",
            "Permissive CORS policy",
            "High",
            "Access-Control-Allow-Origin: *"
        ))

    return findings