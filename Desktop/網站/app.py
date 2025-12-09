from flask import Flask, request, render_template, redirect, url_for, flash, Response
from datetime import datetime
import os
import configparser
app = Flask(__name__)


from flask import Flask
import configparser
import os

app = Flask(__name__)

# 讀 config.ini
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
with open(config_path, encoding="utf-8") as f:
    config.read_file(f)

# 使用設定
app.secret_key = config["app"]["secret_key"]
debug_mode = config["app"].getboolean("debug")

@app.route("/")
def home():
    return "首頁"

if __name__ == "__main__":
    app.run(debug=debug_mode)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-key")  # set env var in production

VISITORS_FILE = "visitors.txt"

def get_remote_addr():
    # 如果在 ngrok 或反向 proxy 下，X-Forwarded-For 會有原始 IP
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        # 可能是一串 IP，取第一個
        return xff.split(",")[0].strip()
    return request.remote_addr or "unknown"

def log_visit(path="/"):
    ip = get_remote_addr()
    ua = request.headers.get("User-Agent", "-")
    now = datetime.utcnow().isoformat() + "Z"
    line = f"{now}\t{ip}\t{path}\t{ua}\n"
    with open(VISITORS_FILE, "a", encoding="utf-8") as f:
        f.write(line)

@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    log_visit("/home")
    return render_template("home.html")

@app.route("/<name>")
def page(name):
    log_visit(f"/{name}")
    # 小心 name 的輸出，Jinja 會自動 escape
    return render_template("page.html", name=name)

@app.route("/material/<name>")
def teacher(name):
    log_visit(f"/{name}")
    # 小心 name 的輸出，Jinja 會自動 escape
    return render_template("teacher.html", name=name)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        log_visit("/contact (POST)")
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        message = request.form.get("message", "")
        # 這裡你可以把表單寫入檔案或寄信（示範寫檔案）
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.utcnow().isoformat()}Z\t{name}\t{email}\t{message}\n")
        flash("感謝你的訊息，我們已收到！")
        return redirect(url_for("contact"))
    else:
        log_visit("/contact (GET)")
        return render_template("contact.html")

if __name__ == "__main__":
    # debug=True 方便開發；正式部署請改為 False 並用 WSGI server
    app.run(host="0.0.0.0", port=5000, debug=False)


#ngrok http 5000這個要執行用cmd


