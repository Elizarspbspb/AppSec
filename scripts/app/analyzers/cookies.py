from models.finding import Finding

def analyze(cookies):
    findings = []

    for c in cookies:
        if not c.secure:
            findings.append(Finding(
                "Cookies",
                f"Cookie '{c.name}' missing Secure flag",
                "Medium",
                "Cookie transmitted over HTTP"
            ))

        if not c.has_nonstandard_attr("HttpOnly"):
            findings.append(Finding(
                "Cookies",
                f"Cookie '{c.name}' missing HttpOnly flag",
                "Medium",
                "Accessible via JavaScript"
            ))

        samesite = c.get_nonstandard_attr("SameSite")
        if not samesite or samesite.lower() == "none":
            findings.append(Finding(
                "Cookies",
                f"Cookie '{c.name}' weak SameSite policy",
                "Medium",
                f"SameSite={samesite}"
            ))

    return findings