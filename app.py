from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    g,
    session
)


class User:
    def __init__(self, ind, username, email, password):
        self.ind = ind
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'{self.username}:{self.ind},{self.email},{self.password}'


users = []
users.append(User(ind=1, username="admin", password="password", email="admin@net"))
users.append(User(ind=2, username="dave", password="secret", email="dave@net"))
users.append(User(ind=3, username="beca", password="sosecret", email="beca@net"))

app = Flask(__name__)
app.secret_key = 'so-secret-key-and-unique'


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.ind == session['user_id']]
        if user:
            g.user = user[0]
        else:
            g.user = None


@app.route('/')
def home_page():
    return redirect(url_for('view_profile'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # error=None
        # if request.form['username'] != user.username or request.form['password'] != user.password:
        # error = 'Invalid credentials.Please try again'
        # else:
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username]
        if user and user[0].password == password:
            session['user_id'] = user[0].ind
            return redirect(url_for('view_profile'))

        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users.append(User(ind=len(users) + 1,
                          username=request.form['username'],
                          password=request.form['password'],
                          email=request.form['email']
                          )
                     )
        print([u.__repr__() for u in users])
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/user', methods=['GET', 'POST'])
def view_profile():
    if request.method == 'POST':
        return redirect(url_for('logout'))
    if not g.user:
        return redirect(url_for('login'))
    return render_template('user.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/update')
def update_profile():
    pass


if __name__ == '__main__':
    app.run(debug=True)
