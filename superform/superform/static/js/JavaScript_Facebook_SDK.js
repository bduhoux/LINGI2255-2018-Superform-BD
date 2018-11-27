
function statusChangeCallBack(response){
    console.log('statusChangeCallback');
    console.log(response);
    if (response.status == 'connected'){
        testAPI();
        p = getPageToken();
        console.log('pagetoken: '+ p);
    } else {
        document.getElementById('status').innerHTML = "Please Log into this app or your post won't be published.";
    }
}

function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallBack(response);
    });
}

window.fbAsyncInit = async function() {
    app_id = await getAppId();
    FB.init({
      appId      : app_id,
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
    FB.api('/me', function (response) {
        console.log('Successful login for: ' + response.name);
        document.getElementById('status').innerHTML =
            'Thanks for logging in, ' + response.name;
    });
}


async function getAppId(){
    var promise1 = await fetch("/appid");
    var data = await promise1.json();
    console.log(data);
    return data;
}

async function getPageId(){
    var promise1 = await fetch("/pageid");
    var data = await promise1.json();
    console.log(data);
    return data;
}

function getPageToken() {
    console.log('getting page token.... ');
    FB.api('/me/accounts?type=page', async function (response) {
        console.log('pageId received');
        pageId = await getPageId();
        response.data.forEach(function (item, index, array) {
            if (item.id == pageId){
                setToken(item.access_token);
            }
        });
    });
}

function setToken(data){
    $.ajax({
       url: '/token',
       data: JSON.stringify({token: data.toString()}),
       dataType: 'json',
       success: function(data) {
            console.log("token received : " + data);
       },
        error: function(err){
           console.log(err);
        },
       type: 'POST'
    });
}
