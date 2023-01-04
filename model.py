from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, DateTime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    username = db.Column(db.String(10), unique=True)

    ratings = db.relationship("Rating", back_populates="user")
    photos = db.relationship("Photo", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"


class Photo(db.Model):
    """A cat photo."""

    __tablename__ = "photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String)
    user_id = db.Column(db.ForeignKey("users.user_id"))
    text = db.Column(db.String)
    name = db.Column(db.String(25))
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())

    ratings = db.relationship("Rating", back_populates="photo")
    user = db.relationship("User", back_populates="photos")

    def __repr__(self):
        return f"<Photo photo_id={self.photo_id} from user_id={self.user_id}>"


class Rating(db.Model):
    """A photo rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    photo_id = db.Column(db.Integer, db.ForeignKey("photos.photo_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    photo = db.relationship("Photo", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"

# class Follow(db.Model):
#     """Follow a user"""

#     __tablename__ = "followings"

#     follow_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     id_of_user_followed = db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     id_of_follower = db.Column(db.Integer, db.ForeignKey("users.user_id"))

#     user_followed = db.relationship("User", foreign_keys=[id_of_user_followed], back_populates="users")
#     user_following = db.relationship("User", foreign_keys=[id_of_follower], back_populates="users")

#     def __repr__(self):
#         return f"<Following id={self.follow_id} following user_id{self.id_of_user_followed} being followed by {self.id_of_follower}>"


def connect_to_db(flask_app, db_uri="postgresql:///cat_rater", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)