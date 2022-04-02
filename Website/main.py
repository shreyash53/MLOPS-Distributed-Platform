from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def welcome():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(port=8001, debug=True)