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

