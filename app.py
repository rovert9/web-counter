import os

from flask import Flask, jsonify
import psycopg2


# Initiate the Flask app
app = Flask(__name__)


# Database connection parameters
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
}


# Creates the "pressed" table
def create_pressed_table():
    try:
        # Creates the database connection
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Creates de pressed table if doesn't exists
        cur.execute('CREATE TABLE IF NOT EXISTS pressed (count INTEGER);')

        # Selects the first row from the "pressed" table
        cur.execute('SELECT 1 FROM pressed LIMIT 1;')

        # If no row exists, insert an initial row with count = 1
        if cur.fetchone() is None:
            cur.execute('INSERT INTO pressed (count) VALUES (1);')

        # Commits the changes to the database
        conn.commit()

    # If there's an error, prints to the consol
    except Exception as e:
        print(str(e))

    # Closes the database connection
    finally:
        if conn:
            conn.close()


# Route to increment the count field from the "pressed" database
@app.route('/api/pressed', methods=['GET'])
def increment_pressed():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Increments the "pressed" table
        cur.execute('UPDATE pressed SET count = count + 1;')
        conn.commit()

        # Gets the updated count
        cur.execute('SELECT count FROM pressed;')
        count = cur.fetchone()[0]

        return jsonify({'count': count})

    # Returns an error if any
    except Exception as e:
        return jsonify({'error': str(e)})

    # Closes the database connection
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    # Create the "pressed" table if it doesn't exist
    create_pressed_table()

    app.run(host='0.0.0.0', port=5000)
