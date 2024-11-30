import pyodbc

# Database connection function
def get_db_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=FaridaAli\SQLEXPRESS;DATABASE=PetLinker;UID=flask_user;PWD=Flask!User1234;TrustServerCertificate=yes')
    return conn

# Function to sign up a new user
def signup_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False  # Username already exists

    # Insert new user with plain text password
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return True  # Successfully signed up

# Function to login a user
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and user[1] == password:  # Assuming password is in index 1
        conn.close()
        return True  # Login successful

    conn.close()
    return False  # Invalid credentials

# Function to edit user profile
def edit_user_profile(username, field, new_value):
    conn = get_db_connection()
    cursor = conn.cursor()

    if field == 'username':
        cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_value, username))
    elif field == 'password':
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_value, username))
    
    conn.commit()
    conn.close()

# Function to delete user profile
def delete_user_profile(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pets WHERE username = ?", (username,))
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

