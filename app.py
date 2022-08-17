from flask import (
    render_template,
    request,
    redirect,
    url_for
)
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from user_model import User
from __init__ import app, login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home_page():
    if current_user.is_authenticated:
        return redirect(url_for('view_profile'))
    return "<h1>Welcome anonymous user profile.</h1><br> Please <a href=/login>login</a> to see your content"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('view_profile'))

    if request.method == 'POST':
        logout_user()
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('view_profile'))
        error = 'Invalid credentials.Try again!'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # NEW USER CREATION
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        email_check = User.query.filter_by(email=email).first()
        user_check = User.query.filter_by(username=username).first()
        if email_check:
            error = 'Email already registered.Try another mail address.'
            return render_template("register.html", error=error)
        elif user_check:
            error = 'Username already taken.Try different.'
            return render_template("register.html", error=error)

        if not (username and email and password):
            error = 'Please fill all the input field'
            return render_template('register.html', error=error)
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', error=error)


@app.route('/user', methods=['GET', 'POST'])
@login_required
def view_profile():
    if request.method == 'POST':
        return redirect(url_for('logout'))

    return render_template('user.html', username=current_user.username, id=current_user.id, email=current_user.email)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/update')
def update_profile():
    pass


if __name__ == '__main__':
    app.run(debug=True)
    # from waitress import serve

    # serve(app, host='127.0.0.1', port=5000)
