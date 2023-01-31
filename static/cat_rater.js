

// const testPhoto = document.querySelector('#photo-upload');
// document.querySelector('#photo-upload').addEventListener('submit', (evt)=>
// {
//     evt.preventDefault();
//     const fileInput = {
//         file : document.querySelector('file').value,
//         text : document.querySelector('#photo-text').value,
//         name : document.querySelector('#photo-name').value
//     };
//     fetch("/myprofile", {
//         method: 'POST',
//         body: JSON.stringify(fileInput),
//         headers: {
//             'Content-Type': 'application/json',
//         },
//     })
//     .then((response) => response.json())
//     .then((responseJson) => {
//         alert(responseJson.status);
//     });
// });


// document.querySelector('#signup').addEventListener('submit', (evt)=>
// {
//     evt.preventDefault();
//     const fileInput = {
//         email : document.querySelector('email').value,
//         password : document.querySelector('password').value,
//         username : document.querySelector('username').value
//     };
//     if (fileInput.email.length < 5){
//         evt.preventDefault();
//         alert("Error, not a valid email")
//     }
//     fetch("/signup", {
//         method: 'POST',
//         body: JSON.stringify(fileInput),
//         headers: {
//             'Content-Type': 'application/json',
//         },
//     })
//     .then((response) => response.json())
//     .then((responseJson) => {
//         alert(responseJson.status);
//     });
// });


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

// document.querySelector('#create-rating').addEventListener('click', (evt)=>
// {
//     evt.preventDefault();

//     const response = confirm("Are you sure you want to create this rating?");

//     if (response) {
        
//         const photoRating = {
//             createRating : document.querySelector('#rating-id').value,
//         };
//         fetch("/photos/<photo_id>", {
//             method: 'POST',
//             body: JSON.stringify(createRating),
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//         })
//         .then((response) => response.json())
//         .then((responseJson) => {
//             alert(responseJson.status);
//         });

//         }
//     }
// );

const container = document.querySelector('.container');
// The Scroll Event.
window.addEventListener('scroll',()=>{
	const {scrollHeight,scrollTop,clientHeight} = document.documentElement;
	if(scrollTop + clientHeight > scrollHeight - 5){
		setTimeout(2000);

	}
});

