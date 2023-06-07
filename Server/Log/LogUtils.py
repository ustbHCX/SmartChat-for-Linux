import time


class Status:
    success = b'0000'
    login_error_pwd = b'0001'
    not_reg = b'0010'
    have_reg = b'0011'
    error_pwd = b'0100'
    have_informed = b'0101'
    not_admin = b'0110'
    member_banned = b'0111'
    online = b'1000'
    undefined = b'1111'


def log(text, status=None):
    if status is not None:
        if status == Status.success:
            tmp = "成功"
        elif status == Status.member_banned:
            tmp = "用户被禁言"
        elif status == Status.not_reg:
            tmp = "用户未注册"
        elif status == Status.online:
            tmp = "用户已经在线"
        elif status == Status.error_pwd:
            tmp = "密码错误"
        elif status == Status.have_reg:
            tmp = "用户已注册"
        elif status == Status.have_informed:
            tmp = "通知已发送"
        elif status == Status.not_admin:
            tmp = "该用户不是管理员"
        elif status == Status.member_banned:
            tmp = "用户被禁言"
        else:
            tmp = "Undefined"
        print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + " " + text + "\t状态: " + tmp)
    else:
        print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + " " + text)
