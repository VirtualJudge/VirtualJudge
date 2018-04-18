function handleRegister(res) {
    $("#id_message").html("");
    console.log(res);
    if (res.status === 0) {
        $("#id_message").attr("class", "text text-success");
        $("#id_message").append("注册成功，两秒后跳转主页");
        setTimeout("location.href='/';", 2000);
    } else {
        $("#id_message").attr("class", "text text-warning");
        $.each(res.data, function (k, v) {
            v.forEach(function (val) {
                $("#id_message").append(val + "\n");
            })
        });
    }
}

function handleButtonClick() {
    registerHandle($("#id_username").val(), $("#id_email").val(), $("#id_password").val(), handleRegister);
}