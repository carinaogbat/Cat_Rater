from flask import (Flask, jsonify, render_template, request, flash, session, redirect)
from model import connect_to_db, db, User, Photo, Rating, connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"



@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/allratings")
def all_photos():
    """View all rated photos."""

    photos = crud.get_all_photos()

    return render_template("all_photos.html", photos=photos)


@app.route("/photos/<photo_id>")
def show_photo(photo_id):
    """Show details on a particular movie."""

    movie = crud.get_photo_by_id(photo_id)

    return render_template("photo_details.html", movie=movie)


@app.route("/users/<username>")
def show_user(username):
    """Show details on a particular user."""

    user = crud.get_user_by_username(username)
    photos = crud.get_users_photos(username)

    return render_template("user_details.html", user=user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)