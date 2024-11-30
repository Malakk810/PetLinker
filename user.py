from flask import Flask, render_template, request, redirect, url_for
from service import signup_user, login_user  # Import service functions

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
                return redirect(url_for('login_signup'))  # Redirect back to the form
            else:
                return render_template('login_signup.html', error="Username already exists!", form_title="Sign Up")

        elif action == 'login':
            # Login Logic
            if login_user(username, password):
                return redirect(url_for('edit_profile', username=username))  # Redirect to profile editing page
            else:
                return render_template('login_signup.html', error="Invalid username or password.", form_title="Log In")

    return render_template('login_signup.html', form_title="Log In")



