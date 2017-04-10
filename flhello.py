from flask import Flask
from flask import redirect

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, world'

@app.route('/<word>')
def google(word):
    return redirect('http://google.com/%s' % word)

if __name__ == '__main__':
    app.run()
