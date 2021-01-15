async function main(){
    async function createMeeting()
    {
        result = await fetch('api/createmeeting?' + new URLSearchParams(
            {
                id: 'CURRENT',
                other_id: window.matchedId
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
    var r = await createMeeting();
    console.log(r);
}
main();