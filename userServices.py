import pyodbc as pydb
from flask import jsonify, redirect, url_for, flash

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

    def create_user(self, data, pet_data):
        try:
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                flash('Username and password are required', 'error')
                return redirect(url_for('user.create_user'))

            if len(password) < 8 or not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
                flash('Password must be at least 8 characters long, including a letter and a number', 'error')
                return redirect(url_for('user.create_user'))

            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Check if username exists
            cursor.execute("SELECT 1 FROM users WHERE username = ?", username)
            if cursor.fetchone():
                flash('Username already exists', 'error')
                return redirect(url_for('user.create_user'))

            # Insert user into database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

            # Insert pet details if provided
            if pet_data:
                cursor.execute(
                    "INSERT INTO pets (username, age, location, breed, history) VALUES (?, ?, ?, ?, ?)",
                    (username, pet_data['age'], pet_data['location'], pet_data['breed'], pet_data['history']),
                )

            conn.commit()
            flash('User profile created successfully!', 'success')
            return redirect(url_for('user.create_user'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('user.create_user'))

        finally:
            conn.close()

    def edit_user_profile(self, username, data, pet_data):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Update username and password if provided
            new_username = data.get('new_username')
            new_password = data.get('new_password')

            if new_username:
                cursor.execute("SELECT 1 FROM users WHERE username = ?", new_username)
                if cursor.fetchone():
                    flash('New username already exists', 'error')
                    return redirect(url_for('user.edit_user_profile', username=username))
                cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, username))
                username = new_username

            if new_password and len(new_password) >= 8 and any(c.isdigit() for c in new_password) and any(c.isalpha() for c in new_password):
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))

            # Update pet details if provided
            if pet_data:
                cursor.execute("UPDATE pets SET age = ?, location = ?, breed = ?, history = ? WHERE username = ?",
                               (pet_data['age'], pet_data['location'], pet_data['breed'], pet_data['history'], username))

            conn.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.edit_user_profile', username=username))

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('user.edit_user_profile', username=username))

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
            flash('User profile deleted successfully!', 'success')
            return redirect(url_for('user.create_user'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('user.create_user'))

        finally:
            conn.close()

