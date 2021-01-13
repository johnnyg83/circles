profileMain()

async function profileMain() {
    var data = await getAllData();
    changeProfile({
        "name": "john boy juice",
        "privacy_settings": "1,2,3,4,5"
    })
    if (data.banned) {
        displayBanned();
    } else {
        displayProfile(data);
        displayButtons();
    }
}

async function getAllData()
{
    result = await fetch('api/user/data?' + new URLSearchParams(
        {
            id: 'CURRENT'
        }), 
        {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
        })
        .then(response => response.json());
    return result
}

function getElement(id) {
    return document.getElementById(id);
}

function displayBanned() {
    getElement('welcome-container').innerText = "You are not welcome, " + data.name + ". You are banned.";
}

function displayProfile(data) {
    let welcome = getElement('welcome-container');
    welcome.innerText = "Welcome, " + data.name + "!";
    let name = getElement('name-container');
    name.innerText = "Name: " + data.name;
    let email = getElement('email-container');
    email.innerText = "Email: " + data.email;
    let pfp = getElement('profile-picture');
    pfp.src = data.image;
    let privacySettings = getElement('privacy-settings-container');
    privacySettings.innerText = "Privacy: " + data.privacy_settings;
    let friends = getElement('friends-container');
    friends.innerText = "Friends: [is an array]";
    let matches = getElement('matches-container');
    matches.innerText = "Matches: [is an array]";
    let blockedUsers = getElement('blocked-users-container');
    blockedUsers.innerText = "Blocked Users: [is an array]";
}

function changeProfile(dict) {
    dict['id'] = 'CURRENT';
    fetch('api/user/changeprofile?' + new URLSearchParams(dict), 
        {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
        });
}

function displayButtons() {
    let pfpButton = document.createElement("BUTTON");
}