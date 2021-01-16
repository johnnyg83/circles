async function createMeeting()
{
    result = await fetch('api/createmeeting?' + new URLSearchParams(
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
    return result;
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
