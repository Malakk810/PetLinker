import pyodbc

class UserService:
    def __init__(self):
        self.db = self.get_db_connection()

    def get_db_connection(self):
        return pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=FaridaAli\\SQLEXPRESS;'
            'DATABASE=PetLinker;'
            'UID=flask_user;'
            'PWD=Flask!User1234;'
            'TrustServerCertificate=yes'
        )

    def create_user(self, data):
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"success": False, "message": "Username and password are required."}
        
        conn = self.db
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return {"success": False, "message": "Username already exists."}

        # Insert user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return {"success": True, "message": "User created successfully."}

    def login_user(self, data):
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"success": False, "message": "Username and password are required."}

        conn = self.db
        cursor = conn.cursor()

        # Check if username and password match
        cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, password))
        if cursor.fetchone():
            return {"success": True, "message": "Login successful."}
        return {"success": False, "message": "Invalid credentials."}

    def edit_user_profile(self, username, data):
        new_username = data.get("username")
        new_password = data.get("password")

        conn = self.db
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if not cursor.fetchone():
            return {"success": False, "message": "User not found."}

        # Update user details
        if new_username:
            cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, username))
        if new_password:
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))

        conn.commit()
        return {"success": True, "message": "User updated successfully."}

    def delete_user_profile(self, username):
        conn = self.db
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if not cursor.fetchone():
            return {"success": False, "message": "User not found."}

        # Delete user from the database
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return {"success": True, "message": "User deleted successfully."}



