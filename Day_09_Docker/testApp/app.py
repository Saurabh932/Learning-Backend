from flask import Flask, render_template
import os
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "index.html",
        hostname=socket.gethostname(),
        env=os.getenv("ENV", "not set")
    )

if __name__ == "__main__":
    print("Server starting...")
    app.run(host="0.0.0.0", port=3000)
