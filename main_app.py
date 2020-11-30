from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, \
                        logout_user


app = Flask(__name__)
app.secret_key = 'afdoi2h3o2380h'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)


class User(UserMixin, db.Model):
    """
        Class for describing user model in database.
        For creating authorising system
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(30), unique=True)


# Function for work with DB and users inside DB
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login')
def login_view():
    """
        Function to display HTML page for GET requests.
    Returns:
        HTML page
    """
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    """
        Function for logging in users
        For POSTS, login the current user by processing the form.

    Returns:
        HTML page
    """
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
        return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """
        Function for logout current user
    """
    logout_user()
    return render_template('logout.html')


@app.route('/')
def index():
    """
        Function that shows main page and amount of times
        visited this page

    Returns:
        visited: amount of visited times of main page
    """
    visited = 0
    if request.cookies.get('visited'):
        visited = int(request.cookies.get('visited'))

    response = make_response(render_template('main.html', visited=visited))
    response.set_cookie('visited', str(visited + 1))
    return response


if __name__ == '__main__':
    app.run(debug=True)
