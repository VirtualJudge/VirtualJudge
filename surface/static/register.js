function handleRegister(res) {
    let message = $("#id_message");
    message.html("");
    console.log(res);
    if (res.status === 0) {
        message.attr("class", "text text-success");
        message.append("注册成功，两秒后跳转主页");
        setTimeout("location.href='/';", 2000);
    } else {
        message.attr("class", "text text-danger");
        $.each(res.data, function (i, item) {
            message.append(item + "\n");
        });
    }
}

function handleButtonClick() {
    let accountObj = new Account();
    let data = {
            'username': $("#id_username").val(),
            'email': $("#id_email").val(),
            'password': $("#id_password").val()
        };
    accountObj.register(handleRegister, data);
}