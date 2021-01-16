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
async function customizeMatchInfo(matchedId){
    otherUserData = await getAllData(matchedId);
    console.log(otherUserData);
    var name = document.getElementById('match-name');
    var description = document.getElementById('match-description');
    var pfp = document.getElementById('match-profile-picture');
    name.innerText = otherUserData['name'];
    var commonInterests = JSON.parse(sessionStorage.getItem('commonInterests'));
    var uncommonInterests = JSON.parse(sessionStorage.getItem('uncommonInterests'));

    var descriptionString = "You're both interested in " + addCommas(commonInterests) + '. Ask ' + otherUserData['name'] + ' about ' + addCommas(uncommonInterests) + '.';
    description.innerText = descriptionString;
    pfp.src = otherUserData['image'];
    matchInfo = document.querySelector('.match-info');
    matchInfo.style.display = 'block';
}
if(sessionStorage.getItem('matchedId') == null){
    window.alert('Could not find matched id.')
}else{
    customizeMatchInfo(sessionStorage.getItem('matchedId'));
}
async function createMeeting()
{
    url = await fetch('api/createmeeting?' + new URLSearchParams(
        {
            id: 'CURRENT',
            other_id: sessionStorage.getItem('matchedId')
        }), 
        {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
        })
        .then(response => response.json());
    return url;
}
async function onCreateMeetingButton(){
    var url = await createMeeting();
    if(url.startsWith("Error")){
        window.alert(url)
    }else{
        var link = document.getElementById('meeting-link');
        link.href = url;
        var meetingInfo = document.getElementById('meeting-info');
        meetingInfo.style.display = 'block'; 
    }
}
function addCommas(arr){
    result = ""
    if(arr.length == 1){
      result += arr[0];
    }
    else if(arr.length > 1){
      for(let i = 0; i < arr.length; i++){
        delimiter = ', ';
        if(i==arr.length - 2){
          if(arr.length == 2){
            delimiter = ' and ';
          }else{
            delimiter = ', and ';
          }
        }else if(i == arr.length - 1){
          delimiter = '';
        }
        result += arr[i];
        result += delimiter;
      }
    }
    return result;
  }
