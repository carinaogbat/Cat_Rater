document.querySelector('#photo-upload').addEventListener('submit', (evt)=>
{
    
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


// document.querySelector('#search-select').addEventListener('submit', (evt)=>
// {
//     evt.preventDefault();
//     const searchInput = {
//         search : document.querySelector('#search-select').value,
//     };
//     fetch("/search", {
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
// })

document.querySelector('#delete-photo').addEventListener('click', (evt)=>
{
    evt.preventDefault();
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
