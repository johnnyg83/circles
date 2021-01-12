get_all_data()



async function get_all_data()
{
    await fetch('api/user/data?' + new URLSearchParams(
        {
            id: 'CURRENT'
        }), 
        {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(function(response){
            data = response
        });

    if (data.banned) {
        document.getElementById('welcome').innerText = "You are not welcome, " + data.name + ". You are banned."
    }
}

