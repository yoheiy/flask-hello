from flask import Flask
from flask import redirect

app = Flask(__name__)

@app.route('/')
def hello():
    return redirect('http://google.com/')

if __name__ == '__main__':
    app.run()
