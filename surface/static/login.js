function handleLogin(res) {
    $("#id_message").html("");
    if (res.status === 0) {
        window.location.href = '/';
    } else {
        $.each(res.data, function (i, item) {
            $("#id_message").append(item + '\n');
        })
    }
}

function handleButtonClick() {
    let obj = new Account();
    let username = $("#id_username").val();
    let password = $("#id_password").val();
    obj.login(username, password, handleLogin);
}

