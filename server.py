from flask import (Flask, jsonify, render_template, request, flash, session, redirect)
from model import connect_to_db, db, User, Photo, Rating, connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def all_photos():
    """View all rated photos."""

    photos = crud.get_all_photos()

    return render_template("homepage.html", photos=photos)

@app.route("/login")
def login():
    """Logs user into the session"""

    return redirect("myprofile/<username>")

@app.route("/signup")
def sign_up():
    """Signs a user up and adds them to the database"""

    return redirect("myprofile/<username>")


@app.route("/photos/<photo_id>")
def show_photo(photo_id):
    """Show details on a particular photo."""

    photo = crud.get_photo_by_id(photo_id)

    return render_template("photo_details.html", photo=photo)

@app.route("/myprofile/<username>")
def show_user_profile(username):
    """Show your profile page"""

    user = crud.get_user_by_username(username)
    photos = crud.get_users_photos(username)
    ratings = crud.get_users_ratings(username)

    return render_template("my_profile.html", user=user, photos=photos, ratings=ratings)

@app.route("/users/<username>")
def show_user(username):
    """Show details on a particular user."""

    user = crud.get_user_by_username(username)
    photos = crud.get_users_photos(username)
    ratings = crud.get_users_ratings(user.user_id)

    return render_template("user_details.html", user=user, photos=photos, ratings=ratings)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)