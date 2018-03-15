## Methods

### problem urls

| url | requests method | view | params | description |
| --- | --- | --- | --- | --- |
| `/vj/problem/<int:problem_id>` | GET | Views.ProblemLocalAPI | | 获取服务器上面已经缓存的题目 |  
| `/vj/problem/<str:remote_oj/<str:remote_id>` | GET | Views.ProblemRemoteAPI | | 从服务器上面获取题目 |
| `/vj/problem/<str:remote_oj>/<str:remote_id>/fresh` | GET | Views.ProblemRemoteAPI | | 从源OJ上面更新服务器上面已经缓存的题目 |
| `/vj/problems/` | GET | Views.ProblemListAPI | | 获取题目列表 |
| `/vj/problems/\<int:offset>` | GET | Views.ProblemListAPI | | 获取题目列表，偏移offset |
| `/vj/problems/<int:offset>/<int:limit>` | GET | Views.ProblemListAPI | | 获取题目列表，偏移offset，每一页limit |

### submission urls
| url | requests method | view | params | description |
| --- | --- | --- | --- | --- |
| `/vj/submission` | POST | views.SubmissionAPI | `<int: problem_id> <str: code> <str: language>` | 提交代码 |
| `/vj/submission/<int:submission_id>` | GET | views.SubmissionShowAPI | | 获取提交的代码 |
| `/vj/submissions` | GET | views.SubmissionListAPI | | 获取提交列表 |
| `/vj/submissions/<int:offset>` | GET | views.SubmissionListAPI | | 获取提交列表 |
| `/vj/rejudge/<int:submission_id>` | GET | views.RejudgeAPI | | 重新提交代码 |
