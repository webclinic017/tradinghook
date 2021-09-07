from flask import render_template, request, flash, session, url_for, redirect
from app import app

@app.route('/logout')
def logout():
    # logout_user()
    return redirect(url_for('welcome'))
    
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'p@$$w0rd':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)