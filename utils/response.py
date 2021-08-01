# 用于Response中默认返回的数据结构
def msg(data=None, err=None, status=0):
    return {
        'status': status,
        'data': data,
        'err': err,
    }
