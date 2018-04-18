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
    loginWebsite($("#id_username").val(), $("#id_password").val(), handleLogin);
}

