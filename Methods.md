## Methods

### account urls

| url | method | view | params | description |
| --- | --- | --- | --- | --- |
| `/api/register` | POST | views.RegisterAPI | `<str: username> <str: password> <str: email>` | 注册 |
| `/api/login` | POST | views.LoginAPI | `<str: username> <str: password>` | 登录 |
| `/api/logout` | GET | views.LogoutAPI| | 退出登录 |

### problem urls

| url | method | view | params | description |
| --- | --- | --- | --- | --- |
| `/api/problem/<int:problem_id>` | GET | Views.ProblemLocalAPI | | 获取服务器上面已经缓存的题目 |  
| `/api/problem/<str:remote_oj/<str:remote_id>` | GET | Views.ProblemRemoteAPI | | 从服务器上面获取题目 |
| `/api/problem/<str:remote_oj>/<str:remote_id>/fresh` | GET | Views.ProblemRemoteAPI | | 从源OJ上面更新服务器上面已经缓存的题目 |
| `/api/problems/` | GET | Views.ProblemListAPI | | 获取题目列表 |
| `/api/problems/\<int:offset>` | GET | Views.ProblemListAPI | | 获取题目列表，偏移offset |
| `/api/problems/<int:offset>/<int:limit>` | GET | Views.ProblemListAPI | | 获取题目列表，偏移offset，每一页limit |

### submission urls
| url | requests method | view | params | description |
| --- | --- | --- | --- | --- |
| `/api/submission` | POST | views.SubmissionAPI | `<int: problem_id> <str: code> <str: language>` | 提交代码 |
| `/api/submission/<int:submission_id>` | GET | views.SubmissionShowAPI | | 获取提交的代码 |
| `/api/submissions` | GET | views.SubmissionListAPI | | 获取提交列表 |
| `/api/submissions/<int:offset>` | GET | views.SubmissionListAPI | | 获取提交列表 |
| `/api/rejudge/<int:submission_id>` | GET | views.RejudgeAPI | | 重新提交代码 |
