/**
 * Created by guoxiao on 16/4/4.
 */
function page_jump(){
    var url = "/preview?page="+$("#page_jump_num").val();
    window.location.replace(url);
}

function loading_begin(loading_message){
    $(".LoadingBg").height(document.body.clientWidth);
    $(".LoadingBg").show();
    $(".LoadingImg").fadeIn(300);
    $(".Loading_message").html("<p>"+loading_message+"</p>")
    //$(".Loading_message").fadeIn(300);

}

function loading_end(){
    $('.LoadingBg, .LoadingImg, .Loading_message').hide();
}

jQuery(function(){

    $(".Close").click(function(){

        $(".LayBg,.LayBox").hide();
    });
    $(".thumbnail").click(function(){
        $(".LayBg").height(document.body.clientWidth);

        $(".LayImg").html($(this).html());

        $(".LayBg").show();
        $(".LayBox").fadeIn(300);

        $(".LayBox").width(640);
        $(".LayBox").height(480);

        $(".LayImg img").width(640);
        $(".LayImg img").height(480);

    });
    var target = document.getElementsByClassName('LoadingImg');
    var spinner = new Spinner().spin(target[0]);


})