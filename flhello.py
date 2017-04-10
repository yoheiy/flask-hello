from flask import Flask
from flask import redirect
from flask import url_for

app = Flask(__name__)

db = {
    0: 'http://flask.pocoo.org/',
    1: 'http://jinja.pocoo.org/',
    2: 'http://werkzeug.pocoo.org/',
}

hello_html = '''<ul>
<li> flask %(flask)s
<li> jinja %(jinja)s
<li> werkzeug %(werkzeug)s
</ul>'''

@app.route('/')
def hello():
    return hello_html % {
            'flask' :    url_for('redir', id=0),
            'jinja' :    url_for('redir', id=1),
            'werkzeug' : url_for('redir', id=2) }

@app.route('/<int:id>')
def redir(id):
    uri = db.get(id) or 'http://www.pocoo.org/'
    return redirect(uri)

if __name__ == '__main__':
    app.run()
