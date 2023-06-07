from Cache import CacheUtils
from Interface import Page
from MessageRecord import RecordUtils
from User import UserUtils
from Utils import Log

from langchain import OpenAI,ConversationChain
# import openai

class Operates:
    add = '1'
    delete = '2'
    confirm = '3'
    refuse = '4'
    ban = '5'
    unban = '6'
    kick = '7'


def execute(cmd, params):
    user = CacheUtils.getCurrentUser()
    # 注册
    if cmd == '/register' or cmd == '/reg':
        # 判断参数是否正确
        if len(params) == 3:
            # 比对二次输入密码是否相同
            if params[1] == params[2]:
                UserUtils.register(params[0], params[1])
            else:
                Log.console("两次输入密码不符")
        else:
            Log.console("格式不符! 正确格式为/register 账号 密码 再次输入密码")

    elif cmd == '/chatgpt' or cmd =='/gpt':
        Log.console("开始chatGPT对话")
        llm = OpenAI(temperature=0)
        conversation = ConversationChain(llm=llm, verbose=True)
        while(1):
            text = input()
            if text == 'exit':
                Log.console("退出chatGPT的对话")
                break
            Log.console(conversation.predict(input=text))



    # 登录
    elif cmd == '/login' or cmd == '/l':
        # 判断参数是否正确
        if len(params) == 2:
            UserUtils.login(params[0], params[1])
            # 判断是否登录成功
            user = CacheUtils.getCurrentUser()
            if user is not None:
                # 页面更新 显示当前通知
                Page.currentUserBoxUpdate(params[0])
                Page.currentContactBoxUpdate("Inform", "")
                Page.messageBoxUpdate(user.getApplicationMessages())
                Page.show()
        else:
            Log.console("格式不符! 正确格式为/login 账号 密码")

    # 修改密码
    elif cmd == '/changepwd' or cmd == '/cp':
        # 判断参数是否正确
        if len(params) == 4:
            # 比对二次输入密码是否相同
            if params[2] == params[3]:
                UserUtils.setPwd(params[0], params[1], params[2])
            else:
                Log.console("两次输入密码不符")
        else:
            Log.console("格式不符! 正确格式为/changepwd 账号 旧密码 新密码 再次输入新密码")

    # 帮助
    elif cmd == '/help':
        Page.clear()
        Log.console("(1)帮助 /help 显示指令 \n"
                    "(2)注册 /register 账号 密码 再次输入密码 或 /reg 账号 密码 再次输入密码\n"
                    "(3)登录 /login 账号 密码 或 /l 账号 密码\n"
                    "(4)退出登录 /logout\n"
                    "(5)修改密码 /changepwd 旧密码 新密码 或 /cp 旧密码 新密码 \n"
                    "(6)添加好友或群聊 /add 目标账号或群号\n"
                    "(7)删除好友或群聊 /del 目标账号或群号\n"
                    "(8)同意通知 /confirm 群号 群通知账号 或 /confirm 好友通知账号\n"
                    "(9)拒绝通知 /refuse 群号 群通知账号 或 /confirm 好友通知账号\n"
                    "(10)群成员禁言 /ban 群号 群成员账号\n"
                    "(11)解禁言 /unban 群号 群成员账号\n"
                    "(12)踢出群成员 /kick 群号 群成员账号\n"
                    "(13)聊天 /c 目标账号或群号 或 /chat 目标账号或群号\n"
                    "(14)ChatGPT对话 /gpt 或 /chatgpt\n"
                    "(15)结束聊天 /end")

    # 登录状态下
    elif user is not None:
        # 聊天
        if cmd == '/chat' or cmd == '/c':
            # 判断参数是否正确
            if len(params) == 1:
                dst = params[0]
                contacts_id = user.getContactsId()
                if dst in contacts_id:
                    # 未读消息设为0
                    user.clearContactUnreadNum(dst)
                    Page.contactsBoxUpdate(user.getContacts())
                    Page.show()
                    # 选中改用户
                    user.setCurrentContactId(dst)
                    Page.currentContactBoxUpdate(user.getContacts()[dst][1], dst)
                    Page.messageBoxUpdate(RecordUtils.getMessages(user.getId(), dst))
                    Page.show()
                else:
                    Log.console("你不是该用户的好友")
            else:
                Log.console("格式不符! 正确格式为/chat 账号")

        # 结束聊天
        elif cmd == "/end":
            # 将当前联系人设置为空 并显示通知页面
            user.setCurrentContactId(None)
            Page.currentContactBoxUpdate("Inform", "")
            Page.messageBoxUpdate(user.getApplicationMessages())
            Page.show()

        # 添加好友/群聊
        elif cmd == '/add':
            # 判断参数是否正确
            if len(params) == 1:
                if params[0] == user.getId():
                    Log.console("你不能添加自己为好友")
                elif params[0] not in user.getContactsId():
                    user.friendOperate(params[0], Operates.add)
                else:
                    Log.console("该好友/群聊已经在你的列表中")
            else:
                Log.console("格式不符! 正确格式为/add 账号")

        # 删除好友
        elif cmd == '/del':
            # 判断参数是否正确
            if len(params) == 1:
                if params[0] in user.getContactsId():
                    user.friendOperate(params[0], Operates.delete)
                    user.delContact(params[0])
                    Page.contactsBoxUpdate(user.getContacts())
                    Page.show()
                    Log.console("您失去了与" + params[0] + "的联系")
                else:
                    Log.console("该好友/群聊不在你的列表中")
            else:
                Log.console("格式不符! 正确格式为/del 账号")

        # 同意好友请求
        elif cmd == '/confirm':
            # 判断参数是否正确
            if len(params) == 1:
                src = params[0]
                if src in user.getFriendApplications():
                    user.friendOperate(src, Operates.confirm)
                    user.delFriendApplication(src)
                    if user.getCurrentContactId() is None:
                        Page.messageBoxUpdate(user.getApplicationMessages())
                        Page.show()

            elif len(params) == 2:
                group = params[0]
                src = params[1]
                if src in user.getGroupApplications(group):
                    user.groupOperate(group, src, Operates.confirm)
                    user.delGroupApplication(group, src)
                    if user.getCurrentContactId() is None:
                        Page.messageBoxUpdate(user.getApplicationMessages())
                        Page.show()
            else:
                Log.console("格式不符! 正确格式为/confirm 账号 或 /confirm 群号 账号")

        # 拒绝好友请求
        elif cmd == '/refuse':
            # 判断参数是否正确
            if len(params) == 1:
                src = params[0]
                if src in user.getFriendApplications():
                    user.friendOperate(src, Operates.refuse)
                    user.delFriendApplication(src)
                    if user.getCurrentContactId() is None:
                        Page.messageBoxUpdate(user.getApplicationMessages())
                        Page.show()
            elif len(params) == 2:
                group = params[0]
                src = params[1]
                if src in user.getGroupApplications(group):
                    user.groupOperate(group, src, Operates.refuse)
                    user.delGroupApplication(group, src)
                    if user.getCurrentContactId() is None:
                        Page.messageBoxUpdate(user.getApplicationMessages())
                        Page.show()
            else:
                Log.console("格式不符! 正确格式为/refuse 账号 或 /refuse 群号 账号")
        # 禁言
        elif cmd == '/ban':
            # 判断参数是否正确
            if len(params) == 2:
                user.groupOperate(params[0], params[1], Operates.ban)
            else:
                Log.console("格式不符! 正确格式为/ban 群号 账号")

        # 解禁言
        elif cmd == '/unban':
            # 判断参数是否正确
            if len(params) == 2:
                user.groupOperate(params[0], params[1], Operates.unban)
            else:
                Log.console("格式不符! 正确格式为/unban 群号 账号")

        # 踢出
        elif cmd == '/kick':
            # 判断参数是否正确
            if len(params) == 2:
                user.groupOperate(params[0], params[1], Operates.kick)
            else:
                Log.console("格式不符! 正确格式为/kick 群号 账号")

        # 登出
        elif cmd == '/logout':
            # 清空页面
            Page.clear()
            # 用户登出
            user.logout()
            # 缓存清空
            CacheUtils.setCurrentUser(None)
