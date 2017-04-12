from flask import Flask
from flask import Markup
from flask import request
from flask import redirect
from flask import url_for
import sqlite3

sql_get = 'select uri from uritab where id = ?'
sql_get_list = 'select * from uritab'
sql_create = 'create table uritab(id integer primary key autoincrement, uri text)'
sql_insert = 'insert into uritab values(null, ?)'

hello_html = '''<title>Short URI demo</title>
<h1>Short URI demo</h1>
<form method='post'>
<input name='uri'>
<input type='submit'>
</form>
'''

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

    def get_list(self):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        ret = cur.execute(sql_get_list).fetchall()
        conn.close()
        return ret

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

    def append(self, uri):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        cur.execute(sql_insert, (uri,))
        conn.commit()
        conn.close()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    d = Database('db')
    if request.method == 'POST':
        d.append(request.form['uri'])
    s = Markup('<ul>')
    for i, u in d.get_list():
        s += Markup("<li><a href='%s'>%d -> %s</a>") % (url_for('redir', id=i), i, u)
    return Markup(hello_html) + s

@app.route('/_<int:id>')
def redir(id):
    d = Database('db')
    uri = d.get(id) or url_for('hello')
    return redirect(uri)

@app.route('/create')
def db_create():
    d = Database('db')
    d.create()
    uri = url_for('hello')
    return redirect(uri)

if __name__ == '__main__':
    app.run()
