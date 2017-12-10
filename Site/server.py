from flask import Flask, render_template, request, session, redirect, make_response, send_file, jsonify


app = Flask(__name__)
app.secret_key = "rate"

@app.route("/")
def index():
    return render_template("page.html")


def main():
    app.run(host="0.0.0.0", port=8666, threaded=True, debug=True)


if __name__ == '__main__':
    main()
