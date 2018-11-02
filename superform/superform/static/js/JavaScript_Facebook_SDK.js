
function statusChangeCallBack(response){
    console.log('statusChangeCallback');
    console.log(response);

    if (response.status == 'connected'){
        testAPI();
    } else {
        document.getElementById('status').innerHTML = "Please Log into this app.";
    }
}

function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallBack(response);
    });
}

window.fbAsyncInit = function() {
FB.init({
  appId      : '317664895679756',
  cookie     : true,
  xfbml      : true,
  version    : 'v3.2'
});

FB.AppEvents.logPageView();

FB.getLoginStatus(function(response) {
    statusChangeCallBack(response);
});
};

(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "https://connect.facebook.net/en_US/sdk.js";
 fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
      document.getElementById('status').innerHTML =
        'Thanks for logging in, ' + response.name;
    });
  }

function getPageToken(){
    console.log('getting page token.... ');
    FB.api('/me/accounts?type=page', function(response) {
        console.log('response received');
        response.data.forEach(function(item, index, array) {
            if (item.name == "Test"){
                console.log(document.getElementById("access_token").value);
            }
        });
    });
}