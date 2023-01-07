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
        if crud.get_photo_rating_average(photo.photo_id) == None:
            rating = "(whoops this kitty has not been rated yet)"
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)

        else:
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
        flash("You are already signed in", category="error")
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
        flash("Error: the email or password you entered was incorrect", category="error")
        return redirect("/login")
    else:
        session["username"] = user.username
        flash(f"Welcome back {user.username}", category="message")

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
        flash("You have been signed out", category="message")
    else:
        flash("Error, you are not signed in", category="error")

    return redirect("/")

@app.route("/signup")
def display_signup():
    """Displays sign up page"""

    user = session.get("username")
    if user:
        flash("You are already signed in", category="message")
        return redirect("/myprofile/<username>")
    else:

        return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def sign_up():
    """Signs a user up and adds them to the database"""

    email = request.form.get("email".lower())
    password = request.form.get("password")
    username = request.form.get("username".lower())

    user = crud.get_user_by_email(email)

    if user:
        flash("Error, there is already an account with this email, please try again", category="error")
        return redirect("/myprofile/<username>")
    else:
        user = crud.create_user(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created", category="message")

    return redirect("/myprofile/<username>")

# @app.route("/photos/<photo_id>")
# def photo_details():
#     """Show details of photo"""

#     return render_template("photo_details.html")

@app.route("/photos/<photo_id>")
def display_photo_details(photo_id):
    """Displays photo details"""

    photo = crud.get_photo_by_id(photo_id)
    if crud.get_photo_rating_average(photo.photo_id) == None:
        photo_rating = "(whoops this kitty has not been rated yet)"
    else:
        photo_average_rating = round(crud.get_photo_rating_average(photo_id))
        photo_rating = photo_average_rating

    return render_template("photo_details.html", photo=photo, photo_rating=photo_rating)


@app.route("/photos/<photo_id>", methods=["POST"])
def show_photo(photo_id):
    """Show details on a particular photo."""

    photo = crud.get_photo_by_id(photo_id)

    if crud.get_photo_rating_average(photo.photo_id) == None:
        photo_rating = "(whoops this kitty has not been rated yet)"
    else:
        photo_average_rating = round(crud.get_photo_rating_average(photo_id))
        photo_rating = photo_average_rating
    username = session.get("username")
    if username is None:
        flash("You must be signed in to rate a cat.", category="message")

    rating = request.form.get("rating")
    if not rating.isdigit():
        flash("Please enter a number between 1 and 10", category="message")
    else:
        user_rating = int(rating)
    # print("*"*35)
    photo_username = crud.get_user_by_id(photo.photo_id)
    # print(photo_username)
    if user_rating > 10 or user_rating < 0:
        flash("Please enter a number between 1 and 10", category="message")
    elif user_rating:
        user = crud.get_user_by_username(username)
        rating = crud.create_rating(user=user, photo=photo, score=user_rating+10)
        db.session.add(rating)
        db.session.commit()
        flash(f"You rated this cat a {rating.score} out of 10!", category="message")
        flash(f'How did we calculate that score? Every cat is AT LEAST a 10 so we added 10 points on!', category="message")

    return render_template("photo_details.html", photo=photo, photo_rating=photo_rating, photo_username=photo_username)

@app.route("/myprofile/<username>")
def display_user_profile(username):
    """Show your profile page"""
    username = session.get("username")
    if username is None:
        flash("Please sign in to see your profile page", category="message")
        return redirect("/login")

    else:
        user = crud.get_user_by_username(username)
        photos = crud.get_users_photos(user.user_id)
        ratings = crud.get_users_ratings(user.user_id)
        photos_with_ratings = []
    for photo in photos:
        if crud.get_photo_rating_average(photo.photo_id) == None:
            rating = "(whoops this kitty has not been rated yet)"
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)

        else:
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
        flash("Please sign in to see your profile page", category="message")
        return redirect("/login")

    else:
        user = crud.get_user_by_username(username)
        photos = crud.get_users_photos(user.user_id)
        ratings = crud.get_users_ratings(user.user_id)
        photos_with_ratings = []
    for photo in photos:
        if crud.get_photo_rating_average(photo.photo_id) == None:
            rating = "(whoops this kitty has not been rated yet)"
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)

        else:
            rating = round(crud.get_photo_rating_average(photo.photo_id)) 
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)

    text = request.form.get("text")
    name = request.form.get("name").capitalize()
    my_file = request.files["my-file"]

    result = cloudinary.uploader.upload(my_file, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    img_url = result['secure_url']
    
    new_photo = crud.create_photo(url=img_url, name=name, text=text, user_id=user.user_id)
    db.session.add(new_photo)
    db.session.commit()


    return render_template("my_profile.html", user=user, photos=photos, ratings=ratings, photos_with_ratings=photos_with_ratings)

@app.route("/users/<username>")
def show_user(username):
    """Show details on a particular user."""

    user = crud.get_user_by_username(username)
    photos = crud.get_users_photos(user.user_id)
    ratings = crud.get_users_ratings(user.user_id)


    photos_with_ratings = []
    for photo in photos:
        if crud.get_photo_rating_average(photo.photo_id) == None:
            rating = "(whoops this kitty has not been rated yet)"
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)

        else:
            rating = round(crud.get_photo_rating_average(photo.photo_id)) 
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)
    

    return render_template("user_details.html", user=user, photos_with_ratings=photos_with_ratings, ratings=ratings, photos=photos)


@app.route("/search")
def display_search():
    """Searches site by user selected parameters""" 

    return render_template("search.html")


@app.route("/search", methods=["POST"])
def search():
    """Searches for user chosen parameters"""

    search_text = request.form.get("search-text")
    search_by = request.form.get("search")
    user = {}

    if search_by == "username":
        user = crud.get_user_by_username(search_text)
    photos_with_ratings = []
    photos = crud.get_photos_by_pet_name(search_text.capitalize())

    for photo in photos:
        if crud.get_photo_rating_average(photo.photo_id) == None:
            rating = "(whoops this kitty has not been rated yet)"
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)

        else:
            rating = round(crud.get_photo_rating_average(photo.photo_id)) 
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)


    # username = request.form.get("username")
    # user_email =request.form.get("user-email")
    # pet_name = request.form.get("pet-name")
    # if username:
    #     user = crud.get_user_by_username(username)
    # elif user_email:
    #     user = crud.get_user_by_email(user_email)
    # pet_name = search_text
    # if pet_name:
    #     pets = crud.get_photos_by_pet_name(pet_name)
    #     print(f'*********{pet_name}******')
    #     print(f'*********{pets}******')
    return render_template("search_results.html", photos_with_ratings=photos_with_ratings, user=user)
    # return f"search: {search_by}   search text: {
    # search_text}"


@app.route("/delete")
def delete():
    """Route to delete photo"""

    return render_template("my_profile.html")

@app.route("/delete", methods=["POST"])
def display():
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
        if crud.get_photo_rating_average(photo.photo_id) == None:
            rating = "(whoops this kitty has not been rated yet)"
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)

        else:
            rating = round(crud.get_photo_rating_average(photo.photo_id)) 
            photo_with_rating = {}
            photo_with_rating['id'] = photo.photo_id
            photo_with_rating['rating'] = rating
            photo_with_rating['username'] = photo.user.username
            photo_with_rating['url'] = photo.url
            photo_with_rating['text'] = photo.text
            photo_with_rating['name'] = photo.name
            photos_with_ratings.append(photo_with_rating)


    delete = request.form.get("photo-id")
    crud.delete_photo_by_id(delete)
    db.session.commit()
    # print("*"*75)
    # print("the value I am printing:")
    # print(delete)

    return render_template("my_profile.html", user=user, photos_with_ratings=photos_with_ratings, ratings=ratings)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)