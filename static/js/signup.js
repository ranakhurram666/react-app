/*
This event is triggering on change in email text box, to check either this email already exist or not.
*/
$("#email").on('change',function(){
    var email = $("#email").val();
    var form_data = new FormData();
    form_data.append('email',email);
    console.log(email);
    $.ajax({
        url: "/email_availability/",
        type: 'GET',
        dataType:'json',
        data:{'email' : email} ,
        cache: false,

        success:function(data){
            console.log(data);
            if(data===true){

                $("#alert_span").text('Valid email.');
                $("#alert_span").css('color', 'green');
            }
            else{
                $("#email").val('');
                $("#alert_span").text('Email already registered.');
                $("#alert_span").css('color', 'red');
            }
        },
        error:function(data){

        }

    });

});

/*
This event is triggering on change in password text box, to check either password has appropriate length or not.
*/
$("#password").on('change',function(){
    if($("#password").val().length < 8){
        $("#password_span").text("Password must be greater than 8 characters.");
        $("#password_span").css('color' , 'red');
        $("#password").val('');
    }
    else {
        $("#password_span").text("");
    }
});

/*
This event is triggering on change in name text box, to check either name has appropriate length or not.
*/
$("#user_name").on('change',function(){
    if($("#user_name").val().length < 3){
        $("#user_name_span").text("Name must be greater than 3 characters.");
        $("#user_name_span").css('color' , 'red');
        $("#user_name").val('');
    }
    else {
        $("#user_name_span").text("");
    }
});
/*
This function is redirecting from signup page to login page when login button clicks
 */

$("#signin-page").on('click',function(e){
    e.preventDefault();
    var host = window.location.host;
    var location = "http://" + host + "/login";
    window.location.replace(location);
});
//$("#signup_form").on('submit',function(){
//$.ajax({
//    url: "/signup/",
//    type: 'POST',
//    processData: false,
//    data: new FormData(this),
//    cache: false,
//    contentType: false,
//    success: function (data) {
//        if(data == "true")
//        {
//
//        }
//        else {
//
//        }
//    },
//    error: function () {
//    }
//});
//});