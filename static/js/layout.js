/*
This is react component of Content Div.
*/

var ContentDiv = React.createClass({
getInitialState: function() {
    return{delete:this.props.data.delete, category: this.props.data.category, path: this.props.data.path, src: this.props.data.path+'.gif', tag: this.props.data.tag, description: this.props.data.description, title: this.props.data.title, image_state:'.gif', image_id:this.props.data.id }
}
,

changeImage:function(){
if(this.state.image_state === '.gif') {
    this.setState({
        src: this.state.path + '.png',
        image_state: '.png'
    });
}
    else{
    this.setState({
        src: this.state.path + '.gif',
        image_state: '.gif'
    });
}
},

render:function(){
    var delete_btn;
    var edit_btn;
    if (this.state.delete == 'yes'){
           delete_btn =   <li><span id="delete-btn" value={this.state.image_id}>Delete</span></li>
           edit_btn =     <li><span id="edit-btn" value={this.state.image_id}>Edit</span></li>
    }
    else{
            delete_btn = '';
            edit_btn = '';
    }

    var temp_text_id ="desc-"+ this.state.image_id;
    var p_id ="p-"+ this.state.image_id;
    var done_btn_id = "done-"+ this.state.image_id;
    var cancel_btn_id = "cancel-"+ this.state.image_id;
    return(

            <div className="blog-post">
            <div>
          <h3>{this.state.title} <small>#{this.state.tag}</small></h3></div>

<img className="thumbnail" src={this.state.src} onClick={this.changeImage}></img>
          <p id={p_id} className="description_para">{this.state.description}</p>
          <textarea className="edit-text-area" id={temp_text_id}>{this.state.description}</textarea>
          <button  id={done_btn_id} className="btn btn-primary edit_btns">Done</button>
          <button  id={cancel_btn_id} className="btn btn-primary edit_btns">Cancel</button>
          <div className="callout">
            <ul className="menu simple">
              <li><a href="#">Category : {this.state.category}</a></li>
                {delete_btn}
                {edit_btn}
            </ul>
          </div>
        </div>
    )


}

})
/*
This is component of ContentList which contains list of content div components.
*/
var ContentList = React.createClass({
render: function() {
    return (
      <div id="contet_list">
        {this.props.data.map(function(result) {
           return <ContentDiv key={result.id} data={result}/>;
        })}
      </div>
    );
  }
})

/*
This function is switching content content on radio button selection.
*/
$("#radios-0, #radios-1").on('change',function(){
    if($(this).is(':checked') && $(this).val() ==2){
        $("#url_div").show();
        $("#file_div").hide();
    }
    else {
        $("#url_div").hide();
        $("#file_div").show();
    }
});

/*
This function is handling edit event, For editing image.
*/
$(document).on('click', '#edit-btn', function (){
    console.log('clicked');
   var edit_image_id = $(this).attr('value');
   $("#p-"+edit_image_id).hide();
   $("#desc-"+edit_image_id).show();
   $("#done-"+edit_image_id).show();
   $("#cancel-"+edit_image_id).show();
   $("#done-"+edit_image_id).on('click',function(){
   var description = $("#desc-"+edit_image_id).val();
   $.ajax({
        url: "/edit",
        type: 'GET',
        dataType: 'json',
        data: {'image_id': edit_image_id, 'text' : description},
        cache: false,

       success: function (data) {

       if(data=="error"){toastr.error("Database Error","Error");
        $("#p-"+edit_image_id).show();
        $("#desc-"+edit_image_id).hide();
        $("#done-"+edit_image_id).hide();
        $("#cancel-"+edit_image_id).hide();}
        else if(data == true){
        $("#p-"+edit_image_id).text(description);
        $("#p-"+edit_image_id).show();
        $("#desc-"+edit_image_id).hide();
        $("#done-"+edit_image_id).hide();
        $("#cancel-"+edit_image_id).hide();
       }
       },

        error:function(){

   }
   });
});
    $("#cancel-"+edit_image_id).on('click',function(){
        $("#p-"+edit_image_id).show();
        $("#desc-"+edit_image_id).hide();
        $("#done-"+edit_image_id).hide();
        $("#cancel-"+edit_image_id).hide();
    });

});

/*
This function is handling signout event, For signout.
*/

$("#signout").on('click',function(e){
    e.preventDefault();
    var host = window.location.host;
    var location = "http://" + host + "/logout";
    window.location.replace(location);
});

/*
This function is handling delete event, For deleting image.
*/
$(document).on('click', '#delete-btn', function (){
    console.log('clicked');
   var delete_image_id = $(this).attr('value');

    $("#delete-dialog-btn").trigger('click');
        $("#delete-btn-ok").on('click',function(){

        $.ajax({
        url: "/delete",
        type: 'GET',
        dataType: 'json',
        data: {'image_id': delete_image_id},
        cache: false,

        success: function (data) {

        if(data=="error"){toastr.error("Database Error","Error");}
        else if(data.length > 0){

        ReactDOM.render( < ContentList
                data = {data} / >, document.getElementById('content_div')
                )
                ;}
        else{
        $("#content_div").html('<div class="no-result">No results found..</div>');

        }

        },
        error: function(){

        }


         });
        $("#delete-btn-cancel").trigger('click');


        });

});

/*
This function is filtering images on basis of selected categories.
*/
$(".list-group-item").on('click',function(e){
    var category = $(this).text();
    console.log(category);
    $.ajax({
        url: "/category",
        type: 'GET',
        dataType: 'json',
        data: {'category': category},
        cache: false,

        success: function (data) {

        if(data=="error"){toastr.error("Database Error","Error"); $("#content_div").html('<div class="no-result">No results found..</div>');}
        else if(data.length > 0){

        ReactDOM.render( < ContentList
                data = {data} / >, document.getElementById('content_div')
                )
                ;}
        else{
        $("#content_div").html('<div class="no-result">No results found..</div>');

        }
        $("#search-btn").prop('disabled', false);
        },
        error: function () {
        }
    });

});


/*
This function is filtering images on the basis of keywords in search box.
*/

$("#search_form").on('submit',function(e) {
    e.preventDefault();
    $("#search-btn").prop('disabled', true);
    var keyword = $("#search_key").val();
    $.ajax({
        url: "/search",
        type: 'GET',
        dataType: 'json',
        data: {'key': keyword},
        cache: false,

        success: function (data) {
        if(data=="error"){toastr.error("Database Error","Error"); $("#content_div").html('<div class="no-result">No results found..</div>');}

if(data.length > 0){

        ReactDOM.render( < ContentList
                data = {data} / >, document.getElementById('content_div')
                )
                ;}
        else{
        $("#content_div").html('<div class="no-result">No results found..</div>');

        }
        $("#search-btn").prop('disabled', false);
        },
        error: function () {
        }
    });

});

/*
This function is uploading image.
*/

$("#upload_form").on('submit',function(e){
    e.preventDefault();
    var alert_message = "";
    $("#success_span").text('');
    var file = document.getElementById("gif");
    if($("#radios-0").is(':checked')) {
        if (!$("#gif").val()) {
            $("#alert_span").text('Select a gif image.');
            alert_message = "alert";
        }
        else if (file.files[0].name.split(".")[file.files[0].name.split(".").length - 1] != "gif") {
            $("#alert_span").text('Choose a gif Image');alert_message = "alert";
        }
    }
    if($("#radios-1").is(':checked')){
        if($("#url").val().split(".")[$("#url").val().split(".").length - 1] != "gif" || $("#url").val()=="" ){
            $("#alert_span").text('Enter a gif Image Url');alert_message = "alert";

        }
    }
    if($("#Image_Title").val()=="" || $("#Image_Tag").val()=="" || $("#Description").val()==""){
        $("#alert_span").text('Fill all fields.');alert_message = "alert";
    }
    if($("#Image_Title").val().length > 15){
        $("#alert_span").text('Image Title should less than 15 characters.');alert_message = "alert";
    }
    if($("#Description").val().length > 150){
        $("#alert_span").text('Description should less than 150 characters.');alert_message = "alert";
    }
    if($("#Image_Tag").val().length > 10){
        $("#alert_span").text('Image Tag should be less than 10 characters.');alert_message = "alert";
    }

    if(alert_message == ""){

        $("#upload").prop('disabled', true);
        var description = $("#Description").val();
        $("#alert_span").text('');
        $("#success_span").text('Uploading...');
        $.ajax({
            url: "/upload/",
            type: 'POST',
            processData: false,

            data: new FormData(this),
            cache: false,
            contentType: false,
            success: function (data) {

        if(data=="error"){toastr.error("Database Error","Error");}
               else {$("#upload").prop('disabled', false);

                ReactDOM.render( < ContentList
                data = {data} / >, document.getElementById('content_div')
                )
                ;}
        $("#gif").val('');
        $("#Description").val('');
        $("#alert_span").text('');
       if(data!="error"){ $("#success_span").text('Image Uploaded Successfully');}
        $("#Image_Tag").val('');
        $("#url").val('');
        $("#Image_Title").val('');
            },
            error: function (xhr, status, err) {
                console.log(xhr);
                $("#upload").prop('disabled', false);
            }
        });
    }
});

/*
This function is loading data when user login.
*/
$(document).ready(function(){
$("#url_div").hide();
$("#delete-dialog").hide();
$.ajax({
    url: "/load_data",
    type: 'GET',
    processData: false,
    cache: false,
    contentType: false,
    success:function(data){

        if(data=="error"){toastr.error("Database Error","Error"); $("#content_div").html('<div class="no-result">No results found..</div>');}
        else if(data.length > 0){

        ReactDOM.render( < ContentList
                data = {data} / >, document.getElementById('content_div')
                )
                ;}
        else{
        $("#content_div").html('<div class="no-result">No results found..</div>');

        }
    },
    error:function(){

    }
});

});
