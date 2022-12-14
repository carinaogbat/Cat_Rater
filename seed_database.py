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
# for photo in data:
#     url, name, text, username = (
#         photo["profile_img"], photo["pet"], photo["bio"], photo["username"]
#     )
#     db_photo = crud.create_photo(url, name, text, username)
#     photos_in_db.append(db_photo)
orion = crud.create_photo(url= "static/imgs/DefaultFloof.jpeg", name= "Orion", text = "A floofy and poofy angel who came to us when she weighed just three ounces!", user_id = 1)
photos_in_db.append(orion)
jeffrey = crud.create_photo(url="static/imgs/Jeffrey.jpg", name="Jeffrey", text= "He was a skinny shelter kitty that started talking the moment we left the shelter and hasnt stopped meow meow all day and especially all night!", user_id=2)
photos_in_db.append(jeffrey)
pablo = crud.create_photo(url= "static/imgs/Pablo.jpg", name= "Pablo", text="", user_id=3)
photos_in_db.append(pablo)
spot = crud.create_photo(url= "static/imgs/Spot.jpg", name= "Spot", text="This is Spot our big boy that we adopted from a shelter. Was very shy and hid from us for about a week. Still little skittish, but loves a belly rub.", user_id=4)
photos_in_db.append(spot)
mac = crud.create_photo(url= "static/imgs/Mac.jpg", name= "Mac", text="", user_id=5)
photos_in_db.append(mac)
leia= crud.create_photo(url= "static/imgs/Leia.jpg", name= "Leia", text="This is Leia she is very loving and a quiet cat", user_id=6)
photos_in_db.append(leia)
zero = crud.create_photo(url= "static/imgs/Zero.jpg", name= "Zero", text="Zero, escape artist, sassy, and moody", user_id=7)
photos_in_db.append(zero)
= crud.create_photo(url= , name= , text=, user_id=8)
photos_in_db.append()
= crud.create_photo(url= , name= , text=, user_id=9)
photos_in_db.append()
= crud.create_photo(url= , name= , text=, user_id=10)
photos_in_db.append()
= crud.create_photo(url= , name= , text=, user_id=11)
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