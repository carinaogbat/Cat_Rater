from flask import (Flask, jsonify, render_template, request, flash, session, redirect)
from model import connect_to_db, db, User, Photo, Rating, connect_to_db
import cloudinary.uploader
import os
import crud
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ["CLOUDINARY_SECRET"]
CLOUD_NAME = "dkiisulmn"

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def all_photos():
    """View all rated photos."""


    photos = crud.get_all_photos()
    photos_with_ratings = []
    for photo in photos:
        rating = round(crud.get_photo_rating_average(photo.photo_id)) 
        photo_with_rating = {}
        photo_with_rating['id'] = photo.photo_id
        photo_with_rating['rating'] = rating
        photo_with_rating['username'] = photo.user.username
        photo_with_rating['url'] = photo.url
        photo_with_rating['text'] = photo.text
        photo_with_rating['name'] = photo.name
        photos_with_ratings.append(photo_with_rating)


    return render_template("homepage.html", photos_with_ratings=photos_with_ratings)

@app.route("/login")
def display_login_page():
    """Displays login page"""

    user_in_session = session.get("username")
    if user_in_session:
        flash("You are already signed in")
        return redirect("/myprofile/<username>")
    else:

        return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """Logs user into the session"""

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("Error: the email or password you entered was incorrect")
        return redirect("/login")
    else:
        session["username"] = user.username
        flash(f"Welcome back {user.username}")

        return redirect("/myprofile/<username>")

@app.route("/logout")
def display_logout():
    """Displays logout page"""

    return render_template("logout.html")

@app.route("/logout", methods=["POST"])
def logout():
    """Logs out a user"""

    user_in_session=session.get("username")
    if user_in_session:
        session["username"] = None
        flash("You have been signed out")
    else:
        flash("Error, you are not signed in")

    return redirect("/")

@app.route("/signup")
def display_signup():
    """Displays sign up page"""

    user = session.get("username")
    if user:
        flash("You are already signed in")
        return redirect("/myprofile/<username>")
    else:

        return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def sign_up():
    """Signs a user up and adds them to the database"""

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")

    user = crud.get_user_by_email(email)

    if user:
        flash("Error, there is already an account with this email, please try again")
        return redirect("/myprofile/<username>")
    else:
        user = crud.create_user(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created")

    return redirect("/myprofile/<username>")

# @app.route("/photos/<photo_id>")
# def photo_details():
#     """Show details of photo"""

#     return render_template("photo_details.html")

@app.route("/photos/<photo_id>")
def display_photo_details(photo_id):
    """Displays photo details"""

    photo = crud.get_photo_by_id(photo_id)

    return render_template("photo_details.html", photo=photo)


@app.route("/photos/<photo_id>", methods=["POST"])
def show_photo(photo_id):
    """Show details on a particular photo."""

    photo = crud.get_photo_by_id(photo_id)
    photo_average_rating = crud.get_photo_rating_average(photo_id)
    username = session.get("username")
    user_rating = int(request.form.get("rating"))

    if username is None:
        flash("Sorry, you must be signed in to rate a cat.")
    elif not user_rating:
        flash("Please enter your rating")
    else:
        user = crud.get_user_by_username(username)

        rating = crud.create_rating(user=user, photo=photo, score=user_rating+10)
        db.session.add(rating)
        db.session.commit()
        flash(f"You rated this cat a {rating} out of 10!")

    return render_template("photo_details.html", photo=photo, photo_rating=photo_average_rating)

@app.route("/myprofile/<username>")
def display_user_profile(username):
    """Show your profile page"""
    username = session.get("username")
    if username is None:
        flash("Please sign in to see your profile page")
        return redirect("/login")

    else:
        user = crud.get_user_by_username(username)
        photos = crud.get_users_photos(user.user_id)
        ratings = crud.get_users_ratings(user.user_id)
        photos_with_ratings = []
        for photo in photos:
            rating = round(crud.get_photo_rating_average(photo.photo_id)) 
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)

    return render_template("my_profile.html", user=user, photos_with_ratings=photos_with_ratings, ratings=ratings)

@app.route("/myprofile/<username>", methods=["POST"])
def show_user_profile(username):
    """Show your profile page"""
    username = session.get("username")
    if username is None:
        flash("Please sign in to see your profile page")
        return redirect("/login")

    else:
        user = crud.get_user_by_username(username)
        photos = crud.get_users_photos(username)
        ratings = crud.get_users_ratings(user.user_id)

    text = request.json.get("text")
    name = request.json.get("name")
    my_file = request.files['my-file']
    result = cloudinary.uploader.upload(my_file, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    img_url = result['secure_url']
    
    new_photo = crud.create_photo(url=img_url, name=name, text=text, username=username)
    db.session.add(new_photo)
    db.session.commit


    return render_template("my_profile.html", user=user, photos=photos, ratings=ratings)

@app.route("/users/<username>")
def show_user(username):
    """Show details on a particular user."""

    user = crud.get_user_by_username(username)
    photos = crud.get_users_photos(user.user_id)
    ratings = crud.get_users_ratings(user.user_id)

    photos_with_ratings = []
    for photo in photos:
        rating = round(crud.get_photo_rating_average(photo.photo_id)) 
        photo_with_rating = {}
        photo_with_rating['id'] = photo.photo_id
        photo_with_rating['rating'] = rating
        photo_with_rating['username'] = photo.user.username
        photo_with_rating['url'] = photo.url
        photo_with_rating['text'] = photo.text
        photo_with_rating['name'] = photo.name
        photos_with_ratings.append(photo_with_rating)
    

    return render_template("user_details.html", user=user, photos_with_ratings=photos_with_ratings, ratings=ratings)

@app.route("/search")
def display_search():
    """Searches site by user selected parameters""" 

    return render_template("search.html")

@app.route("/search", methods=["POST"])

def search():
    """Searches for user chosen parameters"""

    username = request.form.get("username")
    user_email =request.form.get("user-email")
    pet_name = request.form.get("pet-name")

    if username:
        user = crud.get_user_by_username(username)

    elif user_email:
        user = crud.get_user_by_email(user_email)

    elif pet_name:
        pets = crud.get_photos_by_petname(pet_name)


    return redirect("search_results.html", user=user, pets=pets)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)