import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Initializing a Flask app
app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config["DEBUG"] = False

# Initializing a database
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="username",
    password="password",
    hostname="localhost",
    databasename="mailing_list",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Creating a class, User, inherited from the SQLAlchemy model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def add_user(cls, **kw):
        obj = cls(**kw)
        message = "This member has already signed up. Please try again."
        try:
            db.session.add(obj)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(message)

# Creating the app URL route
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('main_page.html', count=User.query.count())
    User.add_user(email = request.form['email'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
