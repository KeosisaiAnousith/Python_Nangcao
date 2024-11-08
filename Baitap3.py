from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="227480201IS003",
            user="postgres",
            password="1234",
            host="localhost",
            port='5432'
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database:", e)
        return None

# Create table if not exists
def create_table():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                year INTEGER NOT NULL,
                genre VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

# Routes
@app.route('/')
def index():
    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM books ORDER BY id")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        genre = request.form['genre']
        
        if not all([title, author, year, genre]):
            return jsonify({"error": "All fields are required"}), 400
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, year, genre) VALUES (%s, %s, %s, %s)",
            (title, author, year, genre)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_book/<int:id>', methods=['POST'])
def update_book(id):
    try:
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        genre = request.form['genre']
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE books SET title=%s, author=%s, year=%s, genre=%s WHERE id=%s",
            (title, author, year, genre, id)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
