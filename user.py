from flask import Flask, render_template, request, redirect, url_for
from service import signup_user, login_user, edit_user_profile, delete_user_profile

app = Flask(__name__)

# Route for login/signup form
@app.route('/login', methods=['GET', 'POST'])
def login_signup():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form['username']
        password = request.form['password']

        if action == 'signup':
            # Sign-up Logic
            if signup_user(username, password):
                return redirect(url_for('login_signup'))  # Redirect back to the form
            else:
                return "Username already exists!"  # Return error if username exists

        elif action == 'login':
            # Login Logic
            if login_user(username, password):
                return redirect(url_for('edit_profile', username=username))  # Redirect to profile editing page
            else:
                return render_template('login_signup.html', error="Invalid username or password.")  # Show error

    return render_template('login_signup.html')

# Route for editing profile
@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        if new_username:
            edit_user_profile(username, 'username', new_username)
            username = new_username

        if new_password:
            edit_user_profile(username, 'password', new_password)

        return redirect(url_for('edit_profile', username=username))

    return render_template('profile.html', username=username)

# Route for deleting the profile
@app.route('/delete_profile/<username>', methods=['POST'])
def delete_profile(username):
    delete_user_profile(username)
    return redirect(url_for('login_signup'))

