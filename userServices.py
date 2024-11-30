from database import Database

class UserService:
    def __init__(self):
        self.db = Database()

    def create_user(self, user_data):
        # Extract user details from JSON payload
        username = user_data.get("username", "").strip()
        password = user_data.get("password", "").strip()
        pet_info = user_data.get("pet", {})

        # Validate username
        if not username:
            return {"success": False, "message": "Username cannot be empty."}
        if self.db.record_exists("SELECT 1 FROM users WHERE username = ?", [username]):
            return {"success": False, "message": "Username already exists."}

        # Validate password
        if len(password) < 8 or not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            return {"success": False, "message": "Password must be at least 8 characters, with at least one letter and one number."}

        # Insert user profile into the database
        self.db.execute("INSERT INTO users (username, password) VALUES (?, ?)", [username, password])

        # If pet information is provided, insert pet details
        if pet_info:
            age = pet_info.get("age")
            location = pet_info.get("location", "").strip()
            breed = pet_info.get("breed", "").strip()
            history = pet_info.get("history", "").strip()

            # Validate pet details
            if not location or not breed or not history or age is None or age < 0:
                return {"success": False, "message": "Invalid pet information provided."}

            self.db.execute(
                "INSERT INTO pets (username, age, location, breed, history) VALUES (?, ?, ?, ?, ?)",
                [username, age, location, breed, history]
            )

        return {"success": True, "message": "User profile created successfully."}

    def edit_user_profile(self, username, update_data):
        # Check if the user exists
        if not self.db.record_exists("SELECT 1 FROM users WHERE username = ?", [username]):
            return {"success": False, "message": "User not found."}

        # Update username if provided and valid
        new_username = update_data.get("username", "").strip()
        if new_username and not self.db.record_exists("SELECT 1 FROM users WHERE username = ?", [new_username]):
            self.db.execute("UPDATE users SET username = ? WHERE username = ?", [new_username, username])
            username = new_username

        # Update password if provided and valid
        new_password = update_data.get("password", "").strip()
        if new_password and len(new_password) >= 8 and any(c.isdigit() for c in new_password) and any(c.isalpha() for c in new_password):
            self.db.execute("UPDATE users SET password = ? WHERE username = ?", [new_password, username])

        # Update pet details if provided
        if update_data.get("pet"):
            pet_info = update_data["pet"]
            if "age" in pet_info and (pet_info["age"] is None or pet_info["age"] < 0):
                return {"success": False, "message": "Invalid pet age provided."}

            if "age" in pet_info:
                self.db.execute("UPDATE pets SET age = ? WHERE username = ?", [pet_info["age"], username])
            if "location" in pet_info:
                self.db.execute("UPDATE pets SET location = ? WHERE username = ?", [pet_info["location"], username])
            if "breed" in pet_info:
                self.db.execute("UPDATE pets SET breed = ? WHERE username = ?", [pet_info["breed"], username])
            if "history" in pet_info:
                self.db.execute("UPDATE pets SET history = ? WHERE username = ?", [pet_info["history"], username])

        return {"success": True, "message": "Profile updated successfully."}

    def delete_user_profile(self, username):
        # Check if the user exists
        if not self.db.record_exists("SELECT 1 FROM users WHERE username = ?", [username]):
            return {"success": False, "message": "User not found."}

        # Delete pet details and user profile
        self.db.execute("DELETE FROM pets WHERE username = ?", [username])
        self.db.execute("DELETE FROM users WHERE username = ?", [username])
        return {"success": True, "message": "Profile deleted successfully."}
