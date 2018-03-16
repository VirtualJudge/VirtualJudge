## Methods

### account urls

| url | method | view | params | description |
| --- | --- | --- | --- | --- |
| `/api/register` | POST | account.views.RegisterAPI | `<str: username> <str: password> <str: email>` | 注册 |
| `/api/login` | POST | account.views.LoginAPI | `<str: username> <str: password>` | 登录 |
| `/api/logout` | GET | account.views.LogoutAPI| | 退出登录 |

### problem urls

| url | method | view | params | description |
| --- | --- | --- | --- | --- |
| `/api/problem/<int:problem_id>` | GET | problem.views.ProblemLocalAPI | | 获取服务器上面已经缓存的题目 |  
| `/api/problem/<str:remote_oj/<str:remote_id>` | GET | problem.views.ProblemRemoteAPI | | 从服务器上面获取题目 |
| `/api/problem/<str:remote_oj>/<str:remote_id>/fresh` | GET | problem.views.ProblemRemoteAPI | | 从源OJ上面更新服务器上面已经缓存的题目 |
| `/api/problems/` | GET | problem.views.ProblemListAPI | | 获取题目列表 |
| `/api/problems/\<int:offset>` | GET | problem.views.ProblemListAPI | | 获取题目列表，偏移offset |
| `/api/problems/<int:offset>/<int:limit>` | GET | problem.views.ProblemListAPI | | 获取题目列表，偏移offset，每一页limit |

### submission urls
| url | requests method | view | params | description |
| --- | --- | --- | --- | --- |
| `/api/submission` | POST | submission.views.SubmissionAPI | `<int: problem_id> <str: code> <str: language>` | 提交代码 |
| `/api/submission/<int:submission_id>` | GET | submission.views.SubmissionShowAPI | | 获取提交的代码 |
| `/api/submissions` | GET | submission.views.SubmissionListAPI | | 获取提交列表 |
| `/api/submissions/<int:offset>` | GET | submission.views.SubmissionListAPI | | 获取提交列表 |
| `/api/rejudge/<int:submission_id>` | GET | submission.views.RejudgeAPI | | 重新提交代码 |
