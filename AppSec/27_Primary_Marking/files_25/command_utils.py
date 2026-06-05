import os


def run_command_template(command):
    prefix = ""
    full = prefix + command
    os.system(full)


def run_maintenance_ping():
    base = "ping -c 1"
    target = "127.0.0.1"
    command = f"{base} {target}"
    os.system(command)
