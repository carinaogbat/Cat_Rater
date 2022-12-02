from model import db, User, Photo, Rating, connect_to_db


def create_user(username, email, password):
    """Creates a User"""

    user = User(username=username, email=email, 
    password=password)

    return user

def create_photo(url, text, username):
    """Creates a photo"""

    photo = Photo(url=url, text=text, username=username)

    return photo

def create_rating(user, photo, score):
    """Scores a photo"""

    rating = Rating(user=user, photo=photo, score=score)

    return rating

def get_user_by_id(user_id):
    """Returns a user by ID"""

    return User.query.get(user_id)

def get_user_by_username(username):
    """Returns a user by Username"""

    return User.query.filter(User.username == username).first()

def get_user_by_email(email):
    """Returns user by email"""

    return User.query.filter(User.email == email).first()

def get_all_users():
    """Return all users"""

    return User.query.all()

def get_all_photos():
    """Returns all photos"""

    return Photo.query.all()

def get_users_photos(username):
    """Returns user photos"""

    return Photo.query.filter(Photo.username == username)

def get_users_ratings(username):
    """Returns user ratings"""


def get_photo_by_id(photo_id):
    """Gets a photo by ID"""

    return Photo.query.get(photo_id)

# if __name__ == '__main__':
#     from server import app
#     connect_to_db(app)

