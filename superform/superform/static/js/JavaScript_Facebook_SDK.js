
function statusChangeCallBack(response){
    console.log('statusChangeCallback');
    console.log(response);

    if (response.status == 'connected'){
        console.log('1');
        //a = getAppId(); // d'abord recup appid
        console.log('2');
        testAPI();
        console.log('3');
        p = getPageToken();
        console.log('4');
        //console.log('appid: '+ a);
        console.log('pagetoken: '+ p);
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
    app_id = getAppId(); //get_appid ici une fois que getappid marche
    console.log("hel");
    console.log(app_id);
    console.log("lo");
    FB.init({
      appId      : '317664895679756',
      //appId      : app_id,
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

/*
function getAppId(){
    $.ajax({
       url: '/appid',
       data: {
          format: 'json'
       },
       dataType: 'json',
       async: !1,
       success: function(data) {
           console.log('printing data...');
           console.log(data);   //comment retoruner ca????
           return data;
       },
       type: 'GET'
    });
}
*/

async function getAppId(){
    var promise1 = await fetch("/appid");
    var data = await promise1.json();
    console.log(data);
    return data;
}



/*
function getAppId(){
    var data;
    fetch("/echo/json").then(function(response){
        data = response.json();
    });
    return data;
}
*/

function getPageToken() {
    console.log('getting page token.... ');
    FB.api('/me/accounts?type=page', function (response) {
        console.log('response received');
        response.data.forEach(function (item, index, array) {
            if (item.name == "Test"){
                /*
                console.log('accesToken: '+item.access_token);
                return item.access_token;
                */
            }
        });
    });
}
