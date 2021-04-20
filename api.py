import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>
Base Url : http://127.0.0.1:5000/<Br>
<Br>
<h2>All Books</h2>
Return all 67 books in our catalogue, in JSON.<br>
<br>
<b>Path : </b>api/v1/resources/books/all<br>
<b>Parameters :</b><br>
<b>Example : </b><br>
<a href="http://127.0.0.1:5000/api/v1/resources/books/all" target="_blank">http://127.0.0.1:5000/api/v1/resources/books/all</a><br>
<br>
<h2>Return a specific book</h2>
Select the books you want by supplying id, year of publication or author.<br>
<br>
<b>Path:</b> /api/v1/resources/books<br>
<b>Parameters:</b><br>
    id : int (id of the book you want to return)<br>
    published : int (year of publication)
    author : str (Author's name) 
<br>
<br>
Return all books by Connie Willis<br>
<a href="http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis" target="_blank">http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis</a><br>
<br>
Return all books by Connie Willis, published in 1999<br>
<a href="http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis&published=1999" target="_blank">http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis&published=1999</a><br>
<br>
Return all books published in 2010<br>
<a href="http://127.0.0.1:5000/api/v1/resources/books?published=2010" target="_blank">http://127.0.0.1:5000/api/v1/resources/books?published=2010</a>'''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'
    print(query)
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


# app.run()
app.run(debug=False)
