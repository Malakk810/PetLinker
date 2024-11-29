from flask import Flask
from config import connect_to_database

app = Flask(__name__)

conn = connect_to_database()
cursor = conn.cursor()

if __name__ == "main":
    app.run(debug=True)
