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

function Account() {
    this.base_url = '/api';
    this.login = function (username, password, callback) {
        let data = {
            'username': username,
            'password': password
        };
        $.post(this.base_url + '/login/', data, function (res) {
            callback(res);
        })
    };
    this.register = function (username, password, email, callback) {
        let data = {
            'username': username,
            'email': email,
            'password': password
        };
        $.post(this.base_url + '/register/', data, function (res) {
            callback(res);
        })
    };
    this.logout = function () {
        $.ajax({
            'url': this.base_url + '/logout/',
            'method': 'DELETE',
        });
    };
    this.session = function (callback) {
        $.post(this.base_url + '/session/', function (res) {
            callback(res);
        })
    };
    this.rank = function (callback) {
        $.post(this.base_url + '/rank/', function (res) {
            callback(res);
        })
    }
}

function Remote() {
    this.base_url = '/api';

    this.support = function (callback) {
        $.post(this.base_url + '/support/', function (res) {
            callback(res);
        })
    };
    this.languages = function (remote_oj, callback) {
        $.post(this.base_url + '/languages/' + remote_oj + '/', function (res) {
            callback(res);
        });
    };
}

function Problem() {
    this.base_url = '/api';
    this.problems = function (callback) {
        $.post(this.base_url + '/problems/', function (res) {
            callback(res);
        })
    };
    this.problem = function (remote_oj, remote_id, callback) {
        $.get(this.base_url + '/problem/' + remote_oj + '/' + remote_id + '/', function (res) {
            callback(res);
        })
    };
}


function Submission() {
    this.base_url = '/api';
    this.submission = function (remote_oj, remote_id, code, language, callback) {
        let data = {
            'remote_oj': remote_oj,
            "remote_id": remote_id,
            "code": code,
            "language": language
        };
        $.post(this.base_url + '/submission/', data, function (res) {
            callback(res);
        });
    };
    this.verdict = function (submission_id, callback) {
        $.post(this.base_url + '/verdict/' + submission_id + '/', function (res) {
            callback(res);
        })
    };
    this.submissions = function (callback) {
        $.post(this.base_url + '/submissions/', function (res) {
            callback(res);
        })
    }
}

function Contest() {
    this.base_url = '/api';
    this.contest = function (data, callback) {
        $.post(this.base_url + '/contest/', data, function (res) {
            callback(res);
        })
    };
    this.contests = function (callback) {
        $.post(this.base_url + '/contests/', function (res) {
            callback(res);
        })
    }
}