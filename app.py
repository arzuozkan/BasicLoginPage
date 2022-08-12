from flask import (
    Flask,
    render_template,
    request, redirect, url_for, g, session
)


class User:
    def __init__(self, index, username, password):
        self.id = index
        self.username = username
        self.password = password


user = User(index=1, username='admin', password='admin')

app = Flask(__name__)
app.secret_key = 'so-secret-key-and-unique'


@app.route('/')
def home_page():
    return 'Welcome '


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != user.username or request.form['password'] != user.password:
            error = 'Invalid credentials.Please try again'
        else:
            session['logged_in'] = True
            return redirect(url_for('view_profile'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/user', methods=['GET', 'POST'])
def view_profile():
    g.username = user.username
    if request.method == 'POST':
        session['logged_in'] = False
        return redirect(url_for('logout'))
    return render_template('user.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/update')
def update_profile():
    pass


if __name__ == '__main__':
    app.run(debug=True)
