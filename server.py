from flask import (Flask, jsonify, render_template, request, flash, session, redirect)
from model import connect_to_db, db, User, Photo, Rating, connect_to_db
from random import choice
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
    
    user_in_session = session.get("username")
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

    return render_template("homepage.html", photos_with_ratings=photos_with_ratings,user_in_session=user_in_session)

@app.route("/login")
def display_login_page():
    """Displays login page"""

    user_in_session = session.get("username")
    if user_in_session:
        flash("You are already signed in", category="message")
        return redirect("/myprofile")
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    """Logs user into the session"""

    content = request.get_json()
    email = content['email']
    print(content)
    #prints {'email': 'OgBot@mail.com', 'password': 'test'}
    password = content['password']
    user = crud.get_user_by_email(email)
    if user and user.password == password:
        session["username"] = user.username
        return (jsonify({'status' : 'ok'}))
    else:
        return (jsonify({'status' : 'invalid email or password'}))

@app.route("/logout")
def display_logout():
    """Displays logout page"""

    return render_template("logout.html")

@app.route("/logout", methods=["POST"])
def logout():
    """Logs out a user"""
    content = request.get_json()
    # logout = content['logout']
    content = request.json
    print('*'*75)
    print('*'*75)
    print(content)
    print('*'*75)
    print('*'*75)
    # print(content)
    # print(content['logout'])
    # # confirm_logout = content['logout']
    # # print(confirm_logout)
    user_in_session=session.get("username")
    if user_in_session:
        session["username"] = None
        return (jsonify({'status' : 'ok'}))
    else: 
        return redirect("/")

@app.route("/signup")
def display_signup():
    """Displays sign up page"""

    user = session.get("username")
    if user:
        flash("You are already signed in", category="message")
        return redirect("/myprofile")
    else:

        return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def sign_up():
    """Signs a user up and adds them to the database"""

    user = session.get("username")
    content = request.get_json()
    email = content['email'].lower()
    username = content['username'].lower()
    password = content['password'].lower()

    if user:
        flash("Error, there is already an account with this email, please try again", category="error")
        return redirect("/myprofile")
    else:
        user = crud.create_user(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created", category="message")

    return jsonify({'status':'ok'})

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
    photo_username = crud.get_user_by_id(photo.photo_id)
    if not rating:
        flash("Please enter a rating before clicking submit")
    if not rating.isdigit():
        flash("Please enter a number between 1 and 10", category="message")
    else:
        user_rating = int(rating)
        if user_rating > 10 or user_rating < 0:
            flash("Please enter a number between 1 and 10", category="message")
        elif user_rating:
            user = crud.get_user_by_username(username)
            rating = crud.create_rating(user=user, photo=photo, score=user_rating+10)
            db.session.add(rating)
            db.session.commit()
            flash(f"You rated this cat a {rating.score} out of 10!", category="rating-score")
            flash(f'How did we calculate that score? Every cat is AT LEAST a 10 so we added 10 points on!', category="rating-message")

    return render_template("photo_details.html", photo=photo, photo_rating=photo_rating, photo_username=photo_username)

@app.route("/myprofile")
def display_user_profile():
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
            photo_with_rating['time_created'] = photo.time_created
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
            photo_with_rating['time_created'] = photo.time_created
            photos_with_ratings.append(photo_with_rating)

            
    return render_template("my_profile.html", user=user, photos_with_ratings=photos_with_ratings, ratings=ratings, username=username)

@app.route("/myprofile", methods=["POST"])
def show_user_profile():
    username = session.get("username")
    """Show your profile page"""
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
            photo_with_rating['time_created'] = photo.time_created
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
            photo_with_rating['time_created'] = photo.time_created
            photos_with_ratings.append(photo_with_rating)

    text = request.form.get("text")
    name = request.form.get("name").capitalize()
    my_file = request.files["my-file"]
    result = cloudinary.uploader.upload(my_file, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    img_url = result['secure_url']
    
    new_photo = crud.create_photo(url=img_url, name=name, text=text, user_id=user.user_id)
    db.session.add(new_photo)
    db.session.commit()

    return render_template("my_profile.html", user=user, photos=photos, ratings=ratings, photos_with_ratings=photos_with_ratings, username=username)

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
    photos_with_ratings = []

    if search_by == "username":
        user = crud.get_user_by_username(search_text)

    if search_by == "pet-name":
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

    return render_template("search_results.html", photos_with_ratings=photos_with_ratings, user=user)



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
   
    content = request.get_json()
    delete = content['deletePhotoId']
    crud.delete_photo_by_id(delete)
    db.session.commit()

    return jsonify({'status': 'ok'})

@app.route("/delete_rating")
def delete_rating():
    """Route to delete rating"""

    return render_template("my_profile.html")

@app.route("/delete_rating", methods=["POST"])
def display_delete():
    username = session.get("username")
    if username is None:
        flash("Please sign in to see your profile page")
        return redirect("/login")
    
    content = request.get_json()
    delete = content['deleteRatingId']
    # print("*"*75)
    # print(delete)
    crud.delete_rating_by_id(delete)
    db.session.commit()

    return jsonify({'status':'ok'})



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)