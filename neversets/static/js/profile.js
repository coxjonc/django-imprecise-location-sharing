//Copyright 2015 Jonathan Cox; MIT License
window.onload = function() {
  $(function() {
    $("#tabs").tabs();
  });
  addSendRequestListener();
  addFriendReqListeners();
  addUnfriendListeners();
  checkExtension();
  window.setTimeout(function(){
    $('.msg').fadeOut('slow')}, 4000
  )
};

/*-------------UTILITIES-----------------
Useful helper functions */

function makeMessage(unique_id, content) {
  var message = document.createElement('div')
  message.className = "msg"
  var textContent = document.createTextNode(content)
  message.appendChild(textContent)
  var title = document.getElementById('siteTitle')
  document.body.insertBefore(message, document.body.firstChild)
  window.setTimeout(function(){
    $('.msg').fadeOut('slow')}, 4000
  )
}

/*    check_newsletter()
    sendFriendRequest()
    check_ext()
    add_friend_req_listeners()
    add_unfriend_listeners()
    add a click event listener to all friend_request elements
}
*/
function makeDialog(unique_id, type, name, msg) {
    var dialog = document.createElement("div")
    var first = document.body.first
    document.body.appendChild(dialog)
    dialog.id = "div_" + unique_id
    if (type=="friend_req") {
        var text = document.createTextNode(name + " sent you a friend request.")
        var span = document.createElement('span')
        span.appendChild(text)
        dialog.appendChild(span)
        $("#"+dialog.id).dialog({
            modal: true,
            resizable: false,
            draggable: false,
            width: 275,
            buttons: [{
                text: "Accept",
                type: "submit",
                form: "accept"
            },
            {
                text: "Decline",
                type: "submit",
                form: "decline"
            }]
        })
    }
    else if (type=="no_ext"){
        var p = document.createElement('p')
        var message = document.createTextNode(msg)
        p.appendChild(message)
        var link = document.createElement('a')
        link.href = "https://chrome.google.com/webstore/detail/sun-never-sets-on-us/hohebpomhmfngamgpmmlchgilecfejgb"
        link.target = "_blank"
        link.appendChild(document.createTextNode("[Go to the Chrome Web Store]"))
        dialog.appendChild(p);
        dialog.appendChild(link)
        $("#"+dialog.id).dialog({
            modal: true,
            resizable: false,
            draggable: false,
            width: 275,
            buttons: {
            'Close' : function() {
            $(this).dialog('close');
            }}
        })
    }
    else if (type=="newsletter"){
        var text = document.createTextNode(msg)
        dialog.appendChild(text)
        $("#"+dialog.id).dialog({
            modal: true,
            resizable: false,
            draggable: false,
            height: 200,
            width: 250,
            buttons: {
            'Close' : function() {
            $(this).dialog('close');
            }}
        })
    }
    else if (type=="unfriend"){
        var text = document.createTextNode("Are you sure you want to unfriend "+ name + "?")
        dialog.appendChild(text)
        $("#"+dialog.id).dialog({
            modal: true,
            resizable: false,
            draggable: false,
            height: 150,
            width: 250,
            buttons: [{
                text: "Unfriend",
                type: "submit",
                form: "unfriend"
            },
            {
                text: "Cancel",
                click: function(){
                    $(this).dialog('close');
                } 
            }]
        })
    }
    $(".ui-dialog-titlebar").hide()
}

/*--------------------Check extension-----------------
Ping extension. If no response, block access to page and
prompt to install extension */
function checkExtension() {
    if(chrome && chrome.runtime && chrome.runtime.sendMessage) {
        console.log("chrome runtime present")
        chrome.runtime.sendMessage(
        "mingiamebfhmhfdgapghhplefcpedohl", 
        {registered: "yes"},function(response) {
            if (!response) {
                console.log('Chrome extension not detected')
                div = document.querySelector('.centerForm')

                h = document.createElement('h2')
                alert = document.createTextNode("Looks like you don't have the location-tracking\
                extension installed yet. You need it to use this site. But don't worry!\
                it takes just seconds to get up and running.")
                h.appendChild(alert)

                h.appendChild(document.createElement('br'))
                h.appendChild(document.createElement('br'))

                var link = document.createElement('a')
                link.href = "https://chrome.google.com/webstore/detail/sun-never-sets-on-us/hohebpomhmfngamgpmmlchgilecfejgb"
                link.appendChild(document.createTextNode("[Go to the Chrome Web Store]"))
                h.appendChild(link)
                $('#loadingTitle').hide()
                div.appendChild(h)
            }
            else {
              console.log(response.success)
              $('#loading').hide()
            }
        });
    };
};

/*-----------------CHECK NEWSLETTER-----------------
Add an event listener to check if a user unchecks the "want newsletter"
checkbox in the settings tab. If they do so, open a dialog box with a 
message.
function check_newsletter() {
    $('#id_want_newsletter').change(function() {
    if (!$(this).prop('checked')) { 
      var unique_id = new Date().getTime().toString()
      var msg = "Are you sure about that? The weekly email is really handy.\
    it never includes ads, and it\'s the easiest way to find out if your friends\' locations change."
      makeDialog(unique_id, 'newsletter', '', msg, true)
    }
  })
}

/*----------------ADD FRIEND REQUEST LISTENERS-------------
If the user clicks one of the friend requests, it will automatically 
populate a hidden form and pop up a modal dialogue prompting user to 
accept or decline */
function addFriendReqListeners() {
    var x = document.querySelectorAll('.friendRequest');
    for (i=0; i<x.length; i++) {
        x[i].addEventListener("click", function(){
           //get the username for each item in the friend list
           var email = jQuery.trim(this.childNodes[3].childNodes[0].nodeValue) 
           var name = this.childNodes[1].childNodes[0].nodeValue
           /*set the hidden accept form and decline form fields to the value of
           the selected name */
           var elem = document.getElementById("id_accept_user")
           elem.value = email
           var elem = document.getElementById("id_decline_user")
           elem.value = email
           //create a unique id for the dialog
           var unique_id = new Date().getTime().toString()
           makeDialog(unique_id, "friend_req", name)
       })
   }
}

/*------------------ADD UNFRIEND LISTENERS-----------------
If the user clicks the "unfriend" button under one of the users in the friend
list, pop up a dialog asking if they want to unfriend that user*/

function addUnfriendListeners() {
    var x = document.querySelectorAll('.unfriend')
    for (i=0; i<x.length; i++) {
        x[i].addEventListener("click", function(){
           //get the username for each item in the friend list
           var email = this.nextSibling.nextSibling.childNodes[0].nodeValue
           /*set the hidden accept form and decline form fields to the value of
           the selected name*/
           var elem = document.getElementById("id_unfriend_user")
           var x = document.querySelector('.unfriend')
           var name = x.parentNode.parentNode.childNodes[1].childNodes[0].childNodes[0].nodeValue
           elem.value = email
           //create a unique id for the dialog
           var unique_id = new Date().getTime().toString()
           makeDialog(unique_id, "unfriend", name)
       })
   }
}
/*-------------------SEND FRIEND REQUEST-------------------
 */


/*-------------------ADD SEND_REQUEST_EVENT LISTENER---------------- 
Add an event listener to the send friend request button that sends data in form field
when clicked. If the user fills out the friend request form and clicks the action button,
send AJAX request to add_friend view and show a message depending on the 
response.
*/
function addSendRequestListener() {
  var button = document.getElementById('sendRequest')
  button.addEventListener('click', function(){
    var email = document.getElementById('id_request_user').value
    $
    friendRequest('/send_request/', email);
  })
}

/*-------------------GET CSRF TOKEN COOKIE------------------------
Use jQuery to get the value of the csrftoken cookie, so that I can submit
friend request form*/
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';')
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i])
      if (cookie.substring(0, name.length+1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue
}

/*-----------------SEND FRIEND REQUEST XHR------------------*/
function friendRequest(url, email) {
  var csrftoken = getCookie('csrftoken')
  var xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = this.response;
      var re = JSON.parse(response)
      unique_id = new Date().getTime().toString()
      makeMessage(unique_id, re.message)
    }
  }

  xhr.withCredentials = true;
  xhr.open('POST', url)
  xhr.setRequestHeader('X-CSRFToken', csrftoken)
  xhr.setRequestHeader('Content-type', "application/x-www-form-urlencoded")
  xhr.send("email=" + email)
}