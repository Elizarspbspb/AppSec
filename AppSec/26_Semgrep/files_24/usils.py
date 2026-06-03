import yaml
import hashlib


def calculate_md5(password):
    m = hashlib.md5()
    m.update(password.encode("utf-8"))
    return m.hexdigest()


def unsafe_yaml_load(raw):
    data = yaml.load(raw)
    return data
