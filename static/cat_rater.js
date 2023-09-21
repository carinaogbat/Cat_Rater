// WORKING LOGIN FORM
const logIn = document.querySelector('#login-form')
if (logIn) {
document.querySelector('#login-form').addEventListener('submit', (evt)=>
{
    evt.preventDefault();
    const loginInput = {
        email : document.querySelector('#login-email').value,
        password : document.querySelector('#login-password').value,
    };
    fetch("/login", {
        method: 'POST',
        body: JSON.stringify(loginInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        if (responseJson.status === 'ok'){
            console.log(responseJson);
            location.assign("/myprofile")
        } 
         else {
            alert('You have entered an invalid password or email, please try again')
        };
        
    });
});
}

// WORKING LOGOUT FORM
const logOut = document.querySelector('#logout-form')
if (logOut) {
document.querySelector('#logout-form').addEventListener('submit', (evt)=>
{
    evt.preventDefault();
    const logoutInput = {
        logout : "true",
    };
    fetch("/logout", {
        method: 'POST',
        body: JSON.stringify(logoutInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        if (responseJson.status === 'ok'){
            console.log(responseJson);
            alert("You have been signed out")
            location.assign("/")
        } else {
            alert('You are not signed in')
        };
        
    });
});
}

// PHOTO UPLOAD FORM (IN PROGRESS)
const photoUpload = document.querySelector('#photo-upload');
if (photoUpload) {
photoUpload.addEventListener('submit', (evt)=>
{
    evt.preventDefault();
    const reader = new FileReader();
    reader.addEventListener('load', (evt) => {
        img.src = evt.target.result;
    });
    const fileInput = {
        file : reader.readAsDataURL('file-upload-button').value,
        text : document.querySelector('#photo-text').value,
        name : document.querySelector('#photo-name').value
    };
    fetch("/myprofile", {
        method: 'POST',
        body: JSON.stringify(fileInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        if (responseJson.status == 'ok'){
            console.log(responseJson);
        };
        
    });
});
};

// WORKING SIGN UP FORM
const signUp = document.querySelector('#signup-form')
if (signUp) { signUp.addEventListener('submit', (evt) =>
{
    evt.preventDefault();
    const signUpPassword = document.querySelector('#signup-password').value;
    const signUpEmail = document.querySelector('#signup-email').value;
    const signUpUsername = document.querySelector('#signup-username').value;

    if (signUpPassword.length < 4) {
        alert("Error: Your password must be at least four characters long.")
    };

    const signUpInput = {
        email : signUpEmail,
        password : signUpPassword,
        username : signUpUsername,
    };
        console.log(signUpInput);
    fetch("/signup", {
        method: 'POST',
        body: JSON.stringify(signUpInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        if (responseJson.status === 'ok'){
            alert("Account successfully created");
            location.assign("/myprofile");
        }
        if (responseJson.status === 'user in database'){
            alert("Error: There is already an account with this username or email, please login or choose a different username.")
        }

    });
});
}

// WORKING PHOTO DELETE FORM
const photoDeleteButtons = document.querySelectorAll('#delete-photo-button')
for (const button of photoDeleteButtons) {

button.addEventListener('click', (evt)=>
{
    evt.preventDefault();
        const response = confirm("Are you sure you want to delete this photo?");
    if (response) {

        const deletePhoto = {
            deletePhotoId : document.querySelector('#photo-id').value,
        };
        fetch("/delete", {
            method: 'POST',
            body: JSON.stringify(deletePhoto),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then((response) => response.json())
        .then((responseJson) => {
            if (responseJson.status == 'ok'){
                // console.log(evt.target.parentElement.parentElement.parentElement)
                evt.target.parentElement.parentElement.parentElement.remove();
            }
        });

        }
    }
);
    
}

// RATING DELETE FORM (IN PROGRESS)
const ratingDeleteButtons = document.querySelectorAll('#delete-rating-button')
for (const button of ratingDeleteButtons) {
button.addEventListener('click', (evt)=>
{
    evt.preventDefault();

    const response = confirm("Are you sure you want to delete this rating?");
    if (response) {
        
        const deleteRating = {
            deleteRatingId : document.querySelector('#rating-id').value,
        };
        fetch("/delete_rating", {
            method: 'POST',
            body: JSON.stringify(deleteRating),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then((response) => response.json())
        .then((responseJson) => {
            if (responseJson.status == 'ok') {
            evt.target.parentElement.parentElement.parentElement.remove()
            }
        });

        }
    }
);
    }

// const ratingForm = document.querySelector('#rating-form')
// if (ratingForm) {
// ratingForm.addEventListener('submit', (evt)=>
// {
//     evt.preventDefault();
//     const ratingInput = {
//         rating : document.querySelector('#rating-value').value,
//     };
//     fetch("/photos/<photo_id>", {
//         method: 'POST',
//         body: JSON.stringify(ratingInput),
//         headers: {
//             'Content-Type': 'application/json',
//         },
//     })
//     .then((response) => response.json())
//     .then((responseJson) => {
//         if (responseJson.status == 'ok'){
//             console.log(responseJson);
//         } else {
//             alert('error')
//         };
        
//     });
// });
// }

// INFINITE SCROLL
const container = document.querySelector('.container');
// The Scroll Event.
window.addEventListener('scroll',()=>{
	const {scrollHeight,scrollTop,clientHeight} = document.documentElement;
	if(scrollTop + clientHeight > scrollHeight - 5){
		setTimeout(2000);

	}
});

