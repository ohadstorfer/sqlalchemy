import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

DATABASE = 'books.db'

# Helper function to initialize the database
def initialize_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create books table
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT
        )
    ''')

    # Create authors table
    c.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

# Function to get book by ID
def get_book_by_id(book_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    conn.close()
    return book

# Function to get author by ID
def get_author_by_id(author_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
    author = c.fetchone()
    conn.close()
    return author

# Route to render index.html
@app.route('/')
def index():
    return render_template('index.html')

# Books CRUD

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')

    if title and author:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book created successfully'}), 201
    else:
        return jsonify({'error': 'Title and author are required'}), 400

@app.route('/books', methods=['GET'])
def list_books():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()

    book_list = [{'id': book[0], 'title': book[1], 'author': book[2]} for book in books]
    return jsonify({'books': book_list}), 200

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_book(book_id):
    book = get_book_by_id(book_id)

    if request.method == 'GET':
        if book:
            return jsonify({'book': {'id': book[0], 'title': book[1], 'author': book[2]}}), 200
        else:
            return jsonify({'error': 'Book not found'}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        new_title = data.get('title')
        new_author = data.get('author')

        if new_title and new_author:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('UPDATE books SET title=?, author=? WHERE id=?', (new_title, new_author, book_id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Book updated successfully'}), 200
        else:
            return jsonify({'error': 'New title and author are required'}), 400

    elif request.method == 'DELETE':
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book deleted successfully'}), 200

# Authors CRUD

@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    author_name = data.get('name')

    if author_name:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Author created successfully'}), 201
    else:
        return jsonify({'error': 'Author name is required'}), 400

@app.route('/authors', methods=['GET'])
def list_authors():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM authors')
    authors = c.fetchall()
    conn.close()

    author_list = [{'id': author[0], 'name': author[1]} for author in authors]
    return jsonify({'authors': author_list}), 200

@app.route('/authors/<int:author_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_author(author_id):
    author = get_author_by_id(author_id)

    if request.method == 'GET':
        if author:
            return jsonify({'author': {'id': author[0], 'name': author[1]}}), 200
        else:
            return jsonify({'error': 'Author not found'}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        new_name = data.get('name')

        if new_name:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('UPDATE authors SET name=? WHERE id=?', (new_name, author_id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Author updated successfully'}), 200
        else:
            return jsonify({'error': 'New author name is required'}), 400

    elif request.method == 'DELETE':
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM authors WHERE id = ?', (author_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Author deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
