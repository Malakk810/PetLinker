from flask import Flask, render_template, request, redirect, url_for
from service import signup_user, login_user, edit_user_profile, delete_user_profile

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login_signup():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form['username']
        password = request.form['password']

        if action == 'signup':
            # Sign-up Logic
            if signup_user(username, password):
                return redirect(url_for('login_signup'))  # Redirect to the same form
            else:
                return render_template('login_signup_profile.html', error="Username already exists!", form_title="Sign Up")

        elif action == 'login':
            # Login Logic
            if login_user(username, password):
                return redirect(url_for('edit_profile', username=username))  # Redirect to profile editing page
            else:
                return render_template('login_signup_profile.html', error="Invalid username or password.", form_title="Log In")

    return render_template('login_signup_profile.html', form_title="Log In")

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

    return render_template('login_signup_profile.html', username=username, form_title="Edit Profile")

@app.route('/delete_profile/<username>', methods=['POST'])
def delete_profile(username):
    delete_user_profile(username)
    return redirect(url_for('login_signup'))  # Redirect back to login/signup page



