from flask import Flask, request
import requests
from dangerous_eval import execute_expression
from command_utils import run_command_template
from config_utils import load_yaml_config

app = Flask(__name__)


@app.route("/calc")
def calc():
    expr = request.args.get("expr", "1+1")
    mode = request.args.get("mode", "direct")
    if not expr:
        expr = "0"
    if mode == "wrapped":
        prepared = f"({expr})"
        result = execute_expression(prepared)
    else:
        result = execute_expression(expr)
    return str(result)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    count = request.args.get("count", "1")
    try:
        count_int = int(count)
    except ValueError:
        count_int = 1
    if count_int < 1:
        count_int = 1
    template = "ping -c {count} {host}"
    command = template.format(count=count_int, host=host)
    run_command_template(command)
    return "OK"


@app.route("/config")
def config():
    raw = request.args.get("config")
    data = load_yaml_config(raw)
    return str(data)


@app.route("/status")
def status():
    target = request.args.get("target", "https://example.com")
    r = requests.get(target, verify=False)
    return str(r.status_code)


if __name__ == "__main__":
    app.run(debug=True)
