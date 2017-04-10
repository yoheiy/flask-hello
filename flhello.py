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
<li> %(flask)s
<li> %(jinja)s
<li> %(werkzeug)s
</ul>'''

def a(word, uri):
    return "<a href='%s'>%s</a>" % (uri, word)

@app.route('/')
def hello():
    return hello_html % {
            'flask' :    a('flask',    url_for('redir', id=0)),
            'jinja' :    a('jinja',    url_for('redir', id=1)),
            'werkzeug' : a('werkzeug', url_for('redir', id=2)) }

@app.route('/_<int:id>')
def redir(id):
    uri = db.get(id) or url_for('hello')
    return redirect(uri)

if __name__ == '__main__':
    app.run()
