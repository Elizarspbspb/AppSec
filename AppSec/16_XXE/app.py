 from flask import Flask, request, render_template, make_response
from lxml import etree

app = Flask(__name__)


PARSER = etree.XMLParser(load_dtd=True, resolve_entities=True, no_network=False)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None, solved=False)

@app.route("/parse", methods=["POST"])
def parse():
    xml_text = request.form.get("xml", "")
    try:
        root = etree.fromstring(xml_text.encode("utf-8"), PARSER)

        flat_text = root.xpath("string()")
        text_lower = flat_text.lower()

        solved_linux = ("root:x:" in text_lower) and ("/bin" in text_lower)

        solved_windows = any(
            marker in text_lower
            for marker in (
                "[fonts]",
                "[extensions]",
                "mci extensions",
                "for 16-bit",
            )
        )

        solved = solved_linux or solved_windows

        return render_template("index.html", result=flat_text, solved=solved)
    except Exception as e:
        resp = make_response(render_template("index.html", result=f"Parse error: {e}", solved=False), 400)
        return resp

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)