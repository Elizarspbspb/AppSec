import yaml

DEFAULT_CONFIG = """
feature_flags:
  beta: false
  logging: true
"""


def load_yaml_config(raw):
    if raw is None or raw.strip() == "":
        text = DEFAULT_CONFIG
    else:
        text = raw
    data = yaml.load(text)
    return data
