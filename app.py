from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, abort
from datetime import datetime
import os
import configparser

app = Flask(__name__)

# ---------------------------
# 訪客紀錄檔案
# ---------------------------
VISITORS_FILE = os.path.join(os.path.dirname(__file__), "visitors.txt")

def get_real_ip():
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr or "unknown"

def log_visit(path="/"):
    ip = get_real_ip()
    ua = request.headers.get("User-Agent", "-")
    now = datetime.utcnow().isoformat() + "Z"
    with open(VISITORS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{now}\t{ip}\t{path}\t{ua}\n")

# ---------------------------
# 防止無效請求
# ---------------------------
@app.before_request
def block_invalid_protocol():
    try:
        request.data
    except Exception:
        return abort(400)

# ---------------------------
# 設定 secret key
# ---------------------------
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
with open(config_path, encoding="utf-8") as f:
    config.read_file(f)

app.secret_key = config["app"]["secret_key"]

# ---------------------------
# 路由
# ---------------------------
@app.route("/")
def index():
    log_visit("/")
    return redirect("/home", code=301)

@app.route("/home/")
def home_slash():
    log_visit("/home/")
    return redirect("/home", code=301)

@app.route("/home")
def home():
    log_visit("/home")
    return render_template("home.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        log_visit("/contact (POST)")
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        message = request.form.get("message", "")
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.utcnow().isoformat()}Z\t{name}\t{email}\t{message}\n")
        flash("感謝你的訊息，我們已收到！")
        return redirect(url_for("contact"))
    else:
        log_visit("/contact (GET)")
        return render_template("contact.html")

@app.route("/<name>")
def page(name):
    log_visit(f"/{name}")
    return render_template("page.html", name=name)

@app.route("/material/<name>")
def teacher(name):
    log_visit(f"/{name}")
    return render_template("teacher.html", name=name)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )


@app.route('/home/google77b51b745d5d14fa.html')
def google_verify_home():
    return send_from_directory('.', 'google77b51b745d5d14fa.html')

# ---------------------------
# 啟動 Flask
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
