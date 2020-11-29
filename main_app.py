from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, \
                        logout_user, current_user


app = Flask(__name__)
app.secret_key = 'afdoi2h3o2380h'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(30), unique=True)


@login_manager.user_loader
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        Function for logging in users
        For GET requests, display the login form. 
        For POSTS, login the current user by processing the form.

    Returns:

    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            print(user.username)
            login_user(user)
            return "You are logged in as {}".format(user.username)

        return 'Wrong password or login'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'asdf'


@login_manager.user_loader
@app.route('/')
def index():
    # username = current_user.username()
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)