document.querySelector('#photo-upload').addEventListener('submit', (evt)=>
{
    evt.preventDefault();
    const fileInput = {
        file : document.querySelector('file').value,
        text : document.querySelector('#photo-text').value,
        name : document.querySelector('#photo-name').value
    };
    fetch("/myprofile/<username>", {
        method: 'POST',
        body: JSON.stringify(fileInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        alert(responseJson.status);
    });
});


document.querySelector('#signup').addEventListener('submit', (evt)=>
{
    evt.preventDefault();
    const fileInput = {
        email : document.querySelector('email').value,
        password : document.querySelector('password').value,
        username : document.querySelector('username').value
    };
    fetch("/signup", {
        method: 'POST',
        body: JSON.stringify(fileInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        alert(responseJson.status);
    });
});


document.querySelector('#delete-photo').addEventListener('click', (evt)=>
{
    evt.preventDefault();

    function confirmDelete(){
        let text = "Do you really want to delete this photo?";
        if (confirm(text) == true) {
            text = "Deleting photo";
        } else {
            text = "Cancelling delete"
        }
    }
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
        alert(responseJson.status);
    });
});

const container = document.querySelector('.container');
// The Scroll Event.
window.addEventListener('scroll',()=>{
	const {scrollHeight,scrollTop,clientHeight} = document.documentElement;
	if(scrollTop + clientHeight > scrollHeight - 5){
		setTimeout(createPost,2000);

	}
});

