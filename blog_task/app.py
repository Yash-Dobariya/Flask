from flask import Flask, render_template

app = Flask(__name__)


@app.route("/main")
def main():
    return render_template(main)


@app.route("/")
def index():
    return "Home page"


@app.route("/register")
def register():
    return "Register page"


@app.route("/login")
def login():
    return "Login page"


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
   
