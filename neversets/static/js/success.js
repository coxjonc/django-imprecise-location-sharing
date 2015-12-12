//copyright Jonathan Cox 2015; MIT License
if(chrome && chrome.runtime && chrome.runtime.sendMessage) {
	console.log("chrome runtime present")
    chrome.runtime.sendMessage(
    "lpcgagekfapeiobknebbcfcnalcjdfcf", 
    {registered: "yes"},function(response) {
    	if (!response) {
    		change_button();
    	};
    });
};

function change_button() {
	button = document.querySelector('.success_button')
	button.value = "Get the Chrome extension"
	success_form = document.querySelector('form')
	success_form.action= "https://chrome.google.com/webstore/detail/sun-never-sets-on-us/hohebpomhmfngamgpmmlchgilecfejg"
	user_message = document.querySelector('p')
	user_message.textContent += " But it looks like you don't have the Chrome location-tracking extension installed.\
	Don't worry - it won't take more than a minute."
};