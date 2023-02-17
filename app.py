from flask import Flask, render_template, request # 導入模組Flask
app = Flask(__name__)  # 呼叫Flask的固定用法


@app.route("/")  # 裝飾器@app.route，之後會解釋
def hello():
    print("it works1")
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    print("it works")
    return render_template('index.html')


if __name__ == "__main__":  # 如果主程式執行
    app.run()  # 啟動伺服器