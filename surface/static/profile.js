function handleGetHookUrl(res) {
    console.log(res);
    if (res.status === 0 && res.data !== null) {
        $("#id_hook_url").val(res.data);
    }
}

function handlePostHookUrl(res) {
    if (res.status === 0) {
        alert(res.data);
    } else {
        alert(res.data);
    }
}

function handlePasswordChange(res) {
    console.log(res);
}

$(document).ready(function () {
    let accountObj = new Account();
    accountObj.hook(handleGetHookUrl, {}, 'GET');
    $("#id_hook_button").click(function () {
        let url = $("#id_hook_url").val();
        if (url !== null && url !== '') {
            accountObj.hook(handlePostHookUrl, {'url': url}, 'POST');
        } else {
            accountObj.hook(handlePostHookUrl, {}, 'DELETE');
        }
    });
});