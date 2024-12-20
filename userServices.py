import pyodbc  # library to connect with MSSQL
class UserService:
    def __init__(self):
        self.db = self.get_db_connection()  #object for database connection

    def get_db_connection(self):
        return pyodbc.connect(
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=FaridaAli\SQLEXPRESS;DATABASE=PetLinker;UID=flask_user;PWD=Flask!User1234;TrustServerCertificate=yes')
        )

    
    def create_user(self, data):
        Username = data.get("username")   #extract the username and password from the data inserted to save it on the database
        Pass_word = data.get("password")
        if not Username or not Pass_word:   #if empty
            return {"success": False, "message": "Username and password are required."}  #success value is here false
        
        conn = self.db  #database connection from the object
        cursor = conn.cursor()  #pointer to let us use database commands and interact with it
                       #returns 1 if userame already exists
        cursor.execute("SELECT 1 FROM UserProfiles WHERE Username = ?", (Username,))   #execute the query to make sure if the username exists on the Userprofile table
        if cursor.fetchone():        #if yes it exists             #? indicates where will the username be inserted, replace the ? with the actual username
            return {"success": False, "message": "Username already exists."}
        cursor.execute("INSERT INTO UserProfiles (Username, Pass_word) VALUES (?, ?)", (Username, Pass_word))
        conn.commit()
        return {"success": True, "message": "User created successfully."}

    def login_user(self, data):
        Username = data.get("username")
        Pass_word = data.get("password")
        if not Username or not Pass_word:
            return {"success": False, "message": "Username and password are required."}

        conn = self.db
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM UserProfiles WHERE Username = ? AND Pass_word = ?", (Username, Pass_word))
        if cursor.fetchone():
            return {"success": True, "message": "Login successful."}
        return {"success": False, "message": "Invalid credentials."}

    def edit_user_profile(self, Username, data):
        new_username = data.get("username")
        new_password = data.get("password")
        conn = self.db
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM UserProfiles WHERE Username = ?", (Username,))
        if not cursor.fetchone():
            return {"success": False, "message": "User not found."}
        if new_username:
            cursor.execute("UPDATE UserProfiles SET Username = ? WHERE Username = ?", (new_username, Username))
        if new_password:
            cursor.execute("UPDATE UserProfiles SET Pass_word = ? WHERE Username = ?", (new_password, Username))

        conn.commit()
        return {"success": True, "message": "User updated successfully."}

    def delete_user_profile(self, Username):
        conn = self.db
        cursor = conn.cursor()

        
        cursor.execute("SELECT 1 FROM UserProfiles WHERE Username = ?", (Username,))
        if not cursor.fetchone():
            return {"success": False, "message": "User not found."}

        
        cursor.execute("DELETE FROM UserProfiles WHERE Username = ?", (Username,))
        conn.commit()
        return {"success": True, "message": "User deleted successfully."}




