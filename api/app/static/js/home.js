var chipSetEl = document.querySelector('.mdc-chip-set');
var chipSet = new mdc.chips.MDCChipSet(chipSetEl);
const matchDialog = new mdc.dialog.MDCDialog(document.querySelector('.mdc-dialog'));
async function getAllData(id)
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
async function match(){
  var matchData = await fetch('api/user/match?' + new URLSearchParams(
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
    .then (function(data){
      return data;
    })
  var ids = matchData['ids'];
  console.log(ids);
  var matchedId = ids[0];
  otherUserData = await getAllData(matchedId);
  console.log(otherUserData);
  customizeMatchDialog(otherUserData, matchData['common_interests'][0].slice(0, 3));
  matchDialog.open();
}
function customizeMatchDialog(otherUserData, commonInterests){
  var dialog = document.querySelector('.mdc-dialog');
  var title = document.getElementById('match-dialog-title');
  var details = document.getElementById('match-dialog-details');
  var image = document.getElementById('match-dialog-image');
  if (otherUserData['image'] != null){
    image.src = otherUserData['image']
  }
  title.innerHTML = 'You matched with ' + otherUserData['name'] + '!';
  if(commonInterests.length == 0){
    detailsString = "";
  }
  else if(commonInterests.length == 1){
    detailsString = "You're both interested in ";
    detailsString += commonInterests[0] + '.';
  }
  else if(commonInterests.length > 1){
    detailsString = "You're both interested in ";
    for(let i = 0; i < commonInterests.length; i++){
      delimiter = ', ';
      if(i==commonInterests.length - 2){
        if(commonInterests.length == 2){
          delimiter = ' and ';
        }else{
          delimiter = ', and ';
        }
      }else if(i == commonInterests.length - 1){
        delimiter = '.';
      }
      detailsString += commonInterests[i];
      detailsString += delimiter;
    }
  }
  details.innerHTML = detailsString;
  console.log(dialog);
}
chipSet.listen('MDCChip:removal',(obj)=>{
  chipId = obj['detail']['chipId'];
  var interest = chipId.substring(chipId.indexOf(" ") + 1);
  deleteCurrentUserInterest(interest);
});

async function getCurrentUserInterests(){
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
        .then (function(data){
            interests = data['interests']
            for(let i = 0; i < interests.length; i++){
              interest = interests[i];
              addChip(interest);
            }
        });
}

getCurrentUserInterests();
function addCurrentUserInterest(interest){
    if (interests.includes(interest)){
        return false;
    }
    interests.push(interest)
    var result = fetch('api/user/addinterest?' + new URLSearchParams(
        {
            id: 'CURRENT',
            interest: interest
        }), 
        {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
        })
        .then(response => response.json());
    return true
}
nChips = 0
function addChip(interest){
  nChips += 1;
  var parent = document.getElementById("mdc-chip-parent");
  var clone = parent.cloneNode(true);
  clone.id += (" " + interest);
  var textNode = clone.querySelector(".mdc-chip__text");
  textNode.innerHTML = interest;
  interestsBox = document.getElementById("chip-box");
  interestsBox.appendChild(clone);
  chipSet.addChip(clone);
}
function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            /*make the matching letters bold:*/
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", async function(e) {
        var a, b, i, val = this.value;
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
          flag = addCurrentUserInterest(val);
          console.log(flag)
          if(flag == true){
            addChip(val);
            this.value = "";
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
  } 


function deleteCurrentUserInterest(interest){
  if (interests.includes(interest)){
    delete interests[interests.indexOf(interest)];
  }
  var result = fetch('api/user/deleteinterest?' + new URLSearchParams(
      {
          id: 'CURRENT',
          interest: interest
      }), 
      {
          method: 'POST',
          headers: {
              'content-type': 'application/json'
          },
      })
      .then(response => response.json());
  return true
}


fetch('api/all/interests', {
  method: 'POST',
  headers: {
    'content-type': 'application/json'
  },
})
.then(response => response.json())
.then (function(data){
    autocomplete(document.getElementById("interests-text-input"), data['all_interests']);
})
.catch(err => console.log(err));