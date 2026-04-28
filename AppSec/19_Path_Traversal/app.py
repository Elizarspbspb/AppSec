import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "dev-secret-key-for-nullbyte-traversal-lab"

BASE_DIR = os.path.join(os.path.dirname(__file__), "images")


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        content=None,
        opened_file=None,
        solved=False,
        error=None,
        requested="",
    )


@app.route("/preview", methods=["GET"])
def preview():
    file_param = (request.args.get("file") or "").strip()
    error = None
    content = None
    opened_file = None
    solved = False

    if not file_param:
        error = "Укажите имя файла."
        return render_template(
            "index.html",
            content=None,
            opened_file=None,
            solved=False,
            error=error,
            requested="",
        )

    if not file_param.endswith(".png"):
        error = "Разрешены только файлы с расширением .png."
        return render_template(
            "index.html",
            content=None,
            opened_file=None,
            solved=False,
            error=error,
            requested=file_param,
        )

    truncated = file_param.split("%00", 1)[0]
    joined = os.path.join(BASE_DIR, truncated)
    real_path = os.path.abspath(joined)
    opened_file = real_path

    try:
        with open(real_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        error = f"Ошибка чтения файла: {e}"
        return render_template(
            "index.html",
            content=None,
            opened_file=opened_file,
            solved=False,
            error=error,
            requested=file_param,
        )

    if "root:x:" in content and "/bin" in content:
        solved = True

    return render_template(
        "index.html",
        content=content,
        opened_file=opened_file,
        solved=solved,
        error=None,
        requested=file_param,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)