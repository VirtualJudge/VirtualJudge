function handleSession(res) {
    let session_url = $("#id_session_ul");
    session_url.html("");
    if (res.status === 0) {
        let header_html = "<li class=\"nav-item\">\n" +
            "<a class=\"nav-link link_profile\" href=\"/profile/\">" + res.data + "</a>\n" +
            "</li>\n" +
            "<li class=\"nav-item\">\n" +
            "<a class=\"nav-link\" id=\"id_logout\" style=\"cursor:pointer;\">登出</a>\n" +
            "</li>";
        session_url.html(header_html);
        $(document).on('click', "#id_logout", handleLogoutClick);
    } else {
        let header_html = "<li class=\"nav-item\">\n" +
            "<a class=\"nav-link\" href=\"/login\">登录</a>\n" +
            "</li>\n" +
            "<li class=\"nav-item\">\n" +
            "<a class=\"nav-link\" href=\"/register\">注册</a>\n" +
            "</li>";
        session_url.html(header_html);
    }
    handleActiveLink();
}

function handleLogoutClick() {
    let accountObj = new Account();
    accountObj.logout();
    location.reload();
}

function handleActiveLink() {
    let url = window.location.pathname.split('/')[1];
    $(".link_" + url).addClass("active");
}

$(document).ready(function () {
    let accountObj = new Account();
    accountObj.session(handleSession);
});
