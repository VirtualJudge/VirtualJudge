function handleLogin(res) {
    $("#id_message").html("");
    console.log(res);
    if (res.status === 0) {
        window.location.href = '/';
    } else {
        $.each(res.data, function (k, v) {
            v.forEach(function (val) {
                $("#id_message").append(val + "\n");
            })
        });
    }
}

function handleButtonClick() {
    let obj = new Account();
    let username = $("#id_username").val();
    let password = $("#id_password").val();
    obj.login(username, password, handleLogin);
}

