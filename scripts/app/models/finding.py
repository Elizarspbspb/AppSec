class Finding:
    def __init__(self, category, title, severity, details, location=None):
        self.category = category
        self.title = title
        self.severity = severity
        self.details = details
        self.location = location

    def __str__(self):
        loc = f" @ {self.location}" if self.location else ""
        return (
            f"[{self.severity}] {self.category}: {self.title}{loc}\n"
            f"    {self.details}"
        )