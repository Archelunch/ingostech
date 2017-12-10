from flask import Flask, render_template, request, session, redirect, make_response, send_file, jsonify
import pandas as pd

app = Flask(__name__)
app.secret_key = "rate"
MAX_FILE_SIZE = 1024 * 1024 + 1

@app.route("/", methods=["POST", "GET"])
def index():
    args = {"method": "GET"}
    if request.method == "POST":
        file = request.files["file"]
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
            f = open('static\\rate\\temp.csv', 'wb')
            f.write(file_bytes)
            f.close()
            data = pd.read_csv('static\\rate\\temp.csv')
            try:
                data['Рейтинг'] = 10 * ((data['Сервис'] * 64.888120787641128 + data['Качество оборудования'] * 284.66963131853748 + data['Профессионализм персонала'] * 122.64878899176045 + data['Стоимость услуг'] * 48.750215387923454) / 2604.7837824293124)
                data = data.sort_values('Рейтинг').iloc[::-1]
                data.to_csv('static/rate/temp1.csv', encoding='UTF-8', index=False)
                data['Рейтинг'] = data['Сервис'] + data['Качество оборудования']  + data['Профессионализм персонала'] + data['Стоимость услуг']*3
                data = data.sort_values('Рейтинг').iloc[::-1]
                data.to_csv('static/rate/temp2.csv', encoding='UTF-8', index=False)
                return render_template("page.html", args={"method": "POST"}, url='rate/temp.csv')
            except Exception as e:
                print(e)
                args["method"] = "Error"
                return render_template("page.html", args=args, url=None)
    return render_template("page.html", args=args, url=None)


def main():
    app.run(host="0.0.0.0", port=8666, threaded=True, debug=True)


if __name__ == '__main__':
    main()
