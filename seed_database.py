import os
import json
import crud
import model
import server
from random import choice, randint

os.system("dropdb cat_rater")
os.system("createdb cat_rater")

model.connect_to_db(server.app)
model.db.create_all()

with open("data/cats.json") as f:
    data = json.loads(f.read())

users_in_db = []
for user in data:
    email, password, username = (
        user["email"], user["password"], user['username']
    )
    db_user = crud.create_user(email, password, username)
    users_in_db.append(db_user)


model.db.session.add_all(users_in_db)
model.db.session.commit()

photos_in_db = []
for photo in data:
    url, name, text, username = (
        photo["profile_img"], photo["pet"], photo["bio"], photo["username"]
    )
    db_photo = crud.create_photo(url, name, text, username)
    photos_in_db.append(db_photo)

model.db.session.add_all(photos_in_db)
model.db.session.commit()

users = crud.get_all_users()
for user in users:
        for photo in photos_in_db:
            score = randint(11, 20)
            rating = crud.create_rating(user=user, photo=photo, score=score)
            model.db.session.add(rating)

model.db.session.commit()



# ogbot_photos_in_db = ["/static/imgs/TiniestFloof.jpeg", "static/imgs/MouseFloof.jpeg", 
#     "static/imgs/YoungFloof.jpeg", "static/imgs/NappingFloof.jpeg", "static/imgs/ComputerFloof.jpeg"]
# jamie_photos_in_db = ["static/imgs/Pepperoni.jpg", "static/imgs/Chloe.jpg", "static/imgs/BlackJack.jpg"]
# lois_photos_in_db = ["static/imgs/Dixie.jpg", "static/imgs/Athena.jpg"]
# chelsea_photos_in_db = ["static/imgs/Mac2ndPhoto.jpg", "static/imgs/Charlie.jpg", "static/imgs/MacAndCharlie.jpg"]

# ogbot = crud.get_user_by_username("OgBot")
# db_photos = []
# for photo_url in ogbot_photos_in_db:
#     db_photo = crud.create_photo(username=ogbot.username, url=photo_url)
#     db_photos.append(db_photo)

# jamie = crud.get_user_by_username("jamie")
# for photo_url in jamie_photos_in_db:
#     db_photo = crud.create_photo(username=jamie.username, url=photo_url)
#     db_photos.append(db_photo)

# lois = crud.get_user_by_username("lois")
# for photo_url in lois_photos_in_db:
#     db_photo = crud.create_photo(lois=lois.username, url=photo_url)
#     db_photos.append(db_photo)

# chelsea = crud.get_user_by_username("chelsea")
# for photo_url in chelsea_photos_in_db:
#     db_photo = crud.create_photo(chelsea=chelsea.username, url=photo_url)
#     db_photos.append(db_photo)


# model.db.session.add_all(db_photos)


model.db.session.commit()