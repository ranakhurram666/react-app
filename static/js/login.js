/*
This event is triggering on submit of login form, to authenticate user.
*/
$("#login_form").on('submit',function(e){
    e.preventDefault();
    var email = $("#email").val();
    var password = $("#password").val();
$.ajax({
    url: "/login/",
    type: 'GET',
    dataType:'json',
    data:{'email' : email, 'password':password} ,
    cache: false,

    success: function (data) {
        if(data == true)
        {
            $("#alert").text('');
            var host = window.location.host;
            var location = "http://" + host + "/layout";
            window.location.replace(location);
        }
        else {
            $("#alert").text('Invalid Username or Password.');
        }
    },
    error: function () {
        console.log("error");
    }
});
});
/*
This function is redirecting from login page to signup page when register button clicks
 */

$("#register-page").on('click',function(e){
    e.preventDefault();
    var host = window.location.host;
    var location = "http://" + host + "/signup";
    window.location.replace(location);
});