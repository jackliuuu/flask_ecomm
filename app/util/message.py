status_msg = {
    200:'成功',
    2000:'異常錯誤',
    10000:'數據不完整',
    10001:'登入功能',
    10011:'用戶名不符合規則',
    10012:'密碼不符合規則',
    10013:'密碼不一致',
    10014:'手機號碼不符合規則',
    10015:'電子信箱不符合規則'
}


def to_dict_msg(status=200,data=None,msg=None):
    return {
        'status':status,
        'data' : data,
        'msg': msg if msg else status_msg.get(status)
    }