from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# python -c 'import secrets; print(secrets.token_hex())'
app.secret_key = '83059b825f5265d8f289ad09c3c5d8155eb6b6f60f0b5dcf762ae8982fce4bf4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# db user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), index=False, unique=True, nullable=False)
    email = db.Column(db.String(20), index=True, unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = set_password(password)


# password storage
def set_password(password):
    return generate_password_hash(password, method='sha256')


# password validation
def check_password(self, password):
    return check_password_hash(self.password, password)


def __repr__(self):
    return '<User {}>'.format(self.username)


"""
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.ind == session['user_id']]
        if user:
            g.user = user[0]
        else:
            g.user = None
"""


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
        if user_check:
            error = 'Username already taken.Try different.'
            return render_template("register.html", error=error)
        new_user = User(username=username,email=email, password=password)
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
    from waitress import serve

    serve(app, host='127.0.0.1', port=8080)
