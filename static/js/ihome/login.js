function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(){

        mobile = $("#mobile").val();
        passwd = $("#password").val();

        $.ajax({
            url: '/user/login/',
            type: 'POST',
            dataType: 'json',
            data: {'mobile': mobile, 'password': passwd},
            success: function (data) {
                if (data.code == '200') {
                    alert(data.msg)
                    location.href = '/user/my/';
                } else {
                    alert(data.msg)
                }
            },
            error: function (data) {
                alert(data.msg)
            }

        });

    });
});