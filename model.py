"""Models for cat rating app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    username = db.Column(db.String(7))

    ratings = db.relationship("Rating", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"


class Photo(db.Model):
    """A cat photo."""

    __tablename__ = "photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    photo_url = db.Column(db.String)
    username = db.Column(db.ForeignKey("users.username"))
    text = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="photo")

    def __repr__(self):
        return f"<Photo photo_id={self.movie_id} from username={self.username}>"


class Rating(db.Model):
    """A photo rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    photo_id = db.Column(db.Integer, db.ForeignKey("photos.photo_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    movie = db.relationship("Photo", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)