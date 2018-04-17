const base_url = '/api';

jQuery(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

function getProblemList(callback) {
    $.post(base_url + '/problems/', function (res) {
        callback(res);
    })
}

function getSupport(callback) {
    $.post(base_url + '/support/', function (res) {
        callback(res);
    })
}

function getProblem(remote_oj, remote_id, who, callback) {
    $.post(base_url + '/problem/' + remote_oj + '/' + remote_id + '/', function (res) {
        callback(res, who);
    })
}

function getLanguageList(remote_oj, callback) {
    $.post(base_url + '/languages/' + remote_oj + '/', function (res) {
        callback(res);
    });
}

function loginWebsite(username, password, callback) {
    $.post(base_url + '/login/', {'username': username, 'password': password}, function (res) {
        callback(res);
    })
}

function registerHandle(username, email, password, callback) {
    $.post(base_url + '/register/', {'username': username, 'email': email, 'password': password}, function (res) {
        callback(res);
    })
}

function getLoginSession(callback) {
    $.post(base_url + '/session/', function (res) {
        callback(res);
    })
}

function getLogout() {
    $.ajax({
        'url': base_url + '/logout/',
        'method': 'DELETE',
    });
}

function submitCode(remote_oj, remote_id, code, language, callback) {
    $.post(base_url + '/submission/', {
        'remote_oj': remote_oj,
        "remote_id": remote_id,
        "code": code,
        "language": language
    }, function (res) {
        callback(res);
    });
}

function getVerdict(submission_id, callback) {
    $.post(base_url + '/verdict/' + submission_id + '/', function (res) {
        callback(res);
    })
}

function getStatusList(callback) {
    $.post(base_url + '/submissions/', function (res) {
        callback(res);
    })
}