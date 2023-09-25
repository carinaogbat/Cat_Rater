# Rate This Cat :cat:
Welcome to Rate This Cat! Rate This Cat! is an entertainment web app for cat lovers around the world that
allows users to upload photos of cats to be rated as well as rate other user submitted cats. Photos are 
uploaded to the application via the Cloudinary API, with most recent photos displaying first through use 
of DateTime. Profile pages display both the cats the user has uploaded and the ratings they've given. 
JavaScript infinite scroll has been implemented to provide a more seamless user experience when loading content,
and most user interactions are handled with AJAX requests. Users are able to create accounts, login and out, upload
and delete photos, create and delete ratings, and view and search other user profiles. You can also view a short
video of the project [here](https://www.youtube.com/watch?v=aQ8SMeggT2w&t=2s).

## About Me
I have spent a large part of my career in healthcare before deciding to make the transition to tech.
I'm so interested and inspired by how much you can create within software development! I do also find
that it is sometimes difficult, but I love the process of logically teasing out your problem and coming
up with a solution. I am intensely curious about how something works or is solved, and am enjoying the process 
of continually learning more.

## Built With
- Python
- Flask
- JavaScript
- Jinja
- Bootstrap
- SQLAlchemy
- CSS
- HTML

## Getting Started
1. Install PostgreSQL
2. Clone or Fork This Repo:
   https://github.com/carinaogbat/Cat_Rater   
3. Create and Activate Virtual Environment:
   ```console
       virtualenv env
       source env/bin/activate
   ```
4. Install The Dependencies:
   ```console
       pip install -r requirements.txt
   ```
5. Sign Up For The Free [Cloudinary API](https://cloudinary.com/documentation/cloudinary_get_started)
6. Set Up The Database:
   ```console
       createdb cat_rater
       python3 model.py
       python3 seed_database.py
   ```
   
7. Run The App:
 ```console
       python3 server.py
   ```
   You can now navigate to 'localhost:5000/' to access Rate This Cat!

## Future Features
Planned future features include following other users and displaying the in a feed as well as editing photo and
rating information.