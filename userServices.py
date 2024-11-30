import pyodbc as pydb
from flask import jsonify

class UserService:
    def get_db_connection(self):
        DB_CONFIG = {
            'DRIVER': 'ODBC Driver 18 for SQL Server',
            'SERVER': 'FaridaAli\\SQLEXPRESS',
            'DATABASE': 'PetLinker',
            'UID': 'flask_user',
            'PWD': 'Flask!User1234',
            'TrustServerCertificate': 'yes',
        }
        conn_str = ';'.join([f'{key}={value}' for key, value in DB_CONFIG.items()])
        return pydb.connect(conn_str)

    def create_user(self, data):
        try:
            username = data.get('username')
            password = data.get('password')
            pet_data = data.get('pet')

            if not username or not password:
                return jsonify({'error': 'Username and password are required'}), 400

            if len(password) < 8 or not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
                return jsonify({'error': 'Password must be at least 8 characters, include a letter and a number'}), 400

            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Check if username exists
            cursor.execute("SELECT 1 FROM users WHERE username = ?", username)
            if cursor.fetchone():
                return jsonify({'error': 'Username already exists'}), 400

            # Insert user into database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

            # Insert pet details if provided
            if pet_data:
                pet_age = pet_data.get('age')
                pet_location = pet_data.get('location')
                pet_breed = pet_data.get('breed')
                pet_history = pet_data.get('history')

                if pet_age is None or pet_age < 0 or not pet_location or not pet_breed or not pet_history:
                    return jsonify({'error': 'Invalid pet details'}), 400

                cursor.execute(
                    "INSERT INTO pets (username, age, location, breed, history) VALUES (?, ?, ?, ?, ?)",
                    (username, pet_age, pet_location, pet_breed, pet_history),
                )

            conn.commit()
            return jsonify({'message': 'User profile created successfully!'}), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            conn.close()

    def edit_user_profile(self, username, data):
        try:
            new_username = data.get('new_username')
            new_password = data.get('new_password')
            new_pet_data = data.get('pet')

            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Update username
            if new_username:
                cursor.execute("SELECT 1 FROM users WHERE username = ?", new_username)
                if cursor.fetchone():
                    return jsonify({'error': 'New username already exists'}), 400
                cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, username))
                username = new_username

            # Update password
            if new_password and len(new_password) >= 8 and any(c.isdigit() for c in new_password) and any(c.isalpha() for c in new_password):
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))

            # Update pet details if provided
            if new_pet_data:
                if 'age' in new_pet_data:
                    cursor.execute("UPDATE pets SET age = ? WHERE username = ?", (new_pet_data['age'], username))
                if 'location' in new_pet_data:
                    cursor.execute("UPDATE pets SET location = ? WHERE username = ?", (new_pet_data['location'], username))
                if 'breed' in new_pet_data:
                    cursor.execute("UPDATE pets SET breed = ? WHERE username = ?", (new_pet_data['breed'], username))
                if 'history' in new_pet_data:
                    cursor.execute("UPDATE pets SET history = ? WHERE username = ?", (new_pet_data['history'], username))

            conn.commit()
            return jsonify({'message': 'Profile updated successfully!'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            conn.close()

    def delete_user_profile(self, username):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Delete pet information
            cursor.execute("DELETE FROM pets WHERE username = ?", username)
            # Delete user information
            cursor.execute("DELETE FROM users WHERE username = ?", username)

            conn.commit()
            return jsonify({'message': 'User profile deleted successfully!'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            conn.close()
