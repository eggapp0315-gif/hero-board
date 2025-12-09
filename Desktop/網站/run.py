import os
import subprocess

def run():
    os.environ["FLASK_APP"] = "app.py"
    os.environ["FLASK_ENV"] = "development"
    subprocess.run(["flask", "run"])

def clean():
    # 刪除 .pyc 檔案
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
        if "__pycache__" in dirs:
            os.rmdir(os.path.join(root, "__pycache__"))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("請使用 python run.py run 或 python run.py clean")
    elif sys.argv[1] == "run":
        run()
    elif sys.argv[1] == "clean":
        clean()
