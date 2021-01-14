profileMain()

async function profileMain() {
    var data = await getAllData();
    if (data.banned) {
        displayBanned();
    } else {
        displayProfile();
        displayButtons();
    }

    async function getAllData(id='CURRENT')
    {
        result = await fetch('api/user/data?' + new URLSearchParams(
            {
                id: id
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

    async function displayProfile() {
        var data = await getAllData();
        let welcomeContainer = getElement('welcome-container');
        welcomeContainer.innerText = "Welcome, " + data.name + "!";
        let nameContainer = getElement('name-container');
        nameContainer.innerText = "Name: " + data.name;
        let emailContainer = getElement('email-container');
        emailContainer.innerText = "Email: " + data.email;
        let pfpContainer = getElement('profile-picture');
        pfpContainer.src = data.image;
        let privacySettingsContainer = getElement('privacy-settings-container');
        privacySettingsContainer.innerText = "Privacy: " + data.privacy_settings;
        displayFriends();
        displayMatches(); 
        displayBlockedUsers();
    }

    async function displayFriends() {
        let friends = await getAllData()
            .then(response => response.friends);
        let friendsContainer = getElement('friends-container');
        for (var i = 0; i < friends.length; i++) {
            let friendDiv = document.createElement("div");
            friendDiv.className = "friend";
            let friendData = await getAllData(friends[i][0])
            friendDiv.innerText = "Friend #" + (i + 1) + ": " + friendData.name + '; Time friended: ' + friends[i][1]; 
            friendsContainer.appendChild(friendDiv);
        }
    }

    async function displayMatches() {
        let matches = await getAllData()
            .then(response => response.matches);
        let matchesContainer = getElement('matches-container');
        for (var i = 0; i < matches.length; i++) {
            let matchesDiv = document.createElement("div");
            matchesDiv.className = "match";
            let matchData = await getAllData(matches[i][0])
            matchesDiv.innerText = "Match #" + (i + 1) + ": " + matchData.name + '; Time matched: ' + matches[i][1]; 
            matchesContainer.appendChild(matchesDiv);
        }
    }

    async function displayBlockedUsers() {
        let blockedUsers = await getAllData()
            .then(response => response.blocked_users);
        let blockedUsersContainer = getElement('blocked-users-container');
        for (var i = 0; i < blockedUsers.length; i++) {
            let blockedUserDiv = document.createElement("div");
            blockedUserDiv.className = "blocked-user";
            let blockedUserData = await getAllData(blockedUsers[i][0])
            blockedUserDiv.innerText = "Blocked user #" + (i + 1) + ": " + blockedUserData.name; 
            blockedUsersContainer.appendChild(blockedUserDiv);
        }
    }

    async function changeProfile(dict) {
        dict['id'] = 'CURRENT';
        await fetch('api/user/changeprofile?' + new URLSearchParams(dict), 
            {
                method: 'POST',
                headers: {
                    'content-type': 'application/json'
                },
            });
        displayProfile()
    }

    function displayButtons() {
        let pfpButton = document.createElement("BUTTON");
    }

}