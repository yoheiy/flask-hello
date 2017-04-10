from flask import Flask
from flask import redirect

app = Flask(__name__)

db = {
    0: 'http://flask.pocoo.org/',
    1: 'http://jinja.pocoo.org/',
    2: 'http://werkzeug.pocoo.org/',
}

hello_html = '''<ul>
<li> 0 flask
<li> 1 jinja
<li> 2 werkzeug
</ul>'''

@app.route('/')
def hello():
    return hello_html

@app.route('/<int:id>')
def google(id):
    uri = db.get(id) or 'http://www.pocoo.org/'
    return redirect(uri)

if __name__ == '__main__':
    app.run()
