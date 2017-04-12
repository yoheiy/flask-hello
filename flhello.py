from flask import Flask
from flask import redirect
from flask import url_for
import sqlite3

sql_get = 'select uri from uritab where id = ?'
sql_create = 'create table uritab(id integer primary key autoincrement, uri text)'
sql_insert = 'insert into uritab values(null, ?)'

db = [
    'http://flask.pocoo.org/',
    'http://jinja.pocoo.org/',
    'http://werkzeug.pocoo.org/',
]
default_uri = 'http://www.pocoo.org/'

hello_html = '<h1>Hello</h1>'

class Database:
    def __init__(self, filename):
        self.filename = filename

    def get(self, id):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        ret = cur.execute(sql_get, (id,)).fetchone()
        conn.close()
        if not ret:
            return default_uri
        return ret[0]

    def create(self):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        try:
            cur.execute(sql_create)
            conn.commit()
        except sqlite3.OperationalError:
            pass
        finally:
            conn.close()

    def insert_sample(self):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        for i in db:
           cur.execute(sql_insert, (i,))
        conn.commit()
        conn.close()

app = Flask(__name__)

@app.route('/')
def hello():
    return hello_html

@app.route('/_<int:id>')
def redir(id):
    d = Database('db')
    uri = d.get(id) or url_for('hello')
    return redirect(uri)

@app.route('/create')
def db_create():
    d = Database('db')
    d.create()
    d.insert_sample()
    uri = url_for('hello')
    return redirect(uri)

if __name__ == '__main__':
    app.run()
