function handleRegister(res) {
    let message = $("#id_message");
    message.html("");
    console.log(res);
    if (res.status === 0) {
        message.attr("class", "text text-success");
        message.append("注册成功，两秒后跳转主页");
        setTimeout("location.href='/';", 2000);
    } else {
        message.attr("class", "text text-warning");
        $.each(res.data, function (k, v) {
            v.forEach(function (val) {
                message.append(val + "\n");
            })
        });
    }
}

function handleButtonClick() {
    let accountObj = new Account();
    accountObj.register($("#id_username").val(), $("#id_email").val(), $("#id_password").val(), handleRegister);
}