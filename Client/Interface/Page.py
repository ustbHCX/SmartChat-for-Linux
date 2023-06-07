import os
import threading

sample = [
    "╔════════════════════════════════════════════════════════════════════════════╦═════════════════╗",
    "║                                                                            ║User:            ║",
    "╟────────────────────────────────────────────────────────────────────────────╫─────────────────╢",
    "║                                                                            ║Online:          ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ╫─────────────────╢",
    "║                                                                            ║Offline:         ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ╫─────────────────╢",
    "║                                                                            ║Group:           ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "║                                                                            ║                 ║",
    "╚════════════════════════════════════════════════════════════════════════════╩═════════════════╝"
]

page = []
lock = threading.Lock()

for k in sample:
    page.append(list(k))


class CurrentUserBox:
    line = 1
    left = 78
    right = 95


def currentUserBoxUpdate(user_id):
    div = page[CurrentUserBox.line]
    index = CurrentUserBox.left
    for i in "User:" + user_id:
        div[index] = i
        index = index + 1
        if index > CurrentUserBox.right:
            break
    while index < CurrentUserBox.right:
        div[index] = " "
        index = index + 1
    page[CurrentUserBox.line] = div


class CurrentContactBox:
    line = 1
    left = 1
    right = 75


def currentContactBoxUpdate(contact_title, contact_id):
    div = page[CurrentContactBox.line]
    index = CurrentContactBox.left
    for i in contact_title + ":" + contact_id:
        div[index] = i
        index = index + 1
        if index > CurrentContactBox.right:
            break
    while index < CurrentContactBox.right:
        div[index] = " "
        index = index + 1
    page[CurrentContactBox.line] = div


class MessageBox:
    left = 1
    right = 75
    top = 3
    bottom = 22
    margin = 5


def messageBoxUpdate(text):
    # 清除页面
    for i in range(MessageBox.left, MessageBox.right + 1):
        for j in range(MessageBox.top, MessageBox.bottom + 1):
            page[j][i] = " "
    if text is None:
        return
    div = page[MessageBox.top:MessageBox.bottom]
    count = 0
    for i in text:
        max_length = 35
        # 获取显示文本
        string = i[2]
        # 获取显示文本长度
        string_length = i[1]
        # 获取消息发送人
        user_id = i[0]
        if string_length < max_length:
            max_length = string_length
        if max_length <= len(user_id):
            max_length = len(user_id) + 1
        # 计算文本框边界
        if user_id == '0':
            end = MessageBox.right - MessageBox.margin
            beg = MessageBox.right - max_length - MessageBox.margin
        else:
            end = MessageBox.left + max_length + MessageBox.margin
            beg = MessageBox.left + MessageBox.margin
        # 添加上边框
        line = list(div[count])
        line[beg - 1] = "╭"
        for j in range(0, max_length + 1):
            line[beg + j] = "┉"
        line[end + 1] = "╮"
        # 获取消息发送人，并获取显示方式
        if user_id == '0':
            line[end + 1] = "╳"
        elif user_id == '1':
            line[beg - 1] = "╳"
        else:
            line[beg - 1] = "╳"
            for j in range(0, len(user_id)):
                line[beg + j + 1] = user_id[j]
        div[count] = line
        # 下一行
        count = count + 1
        line = list(div[count])
        pos = beg
        # 左边框
        line[pos - 1] = "│"
        # 显示文本
        for j in string:
            line[pos] = j
            if isChinese(j):
                pos = pos + 1
                line[pos] = ""
            pos = pos + 1
            if pos > end:
                # 右边框
                line[pos] = "│"
                div[count] = line
                # 下一行左边框
                count = count + 1
                line = list(div[count])
                pos = beg
                line[pos - 1] = "│"
        # 右边框
        line[end + 1] = "│"

        # 下一行
        div[count] = line
        count = count + 1
        line = list(div[count])
        line[beg - 1] = "╰"
        for j in range(0, max_length + 1):
            line[beg + j] = "┉"
        line[end + 1] = "╯"
        # 下一条
        div[count] = line
        count = count + 1
    # 保存
    page[MessageBox.top:MessageBox.bottom] = div


class ContactsBox:
    online_top = 4
    online_bottom = 10
    offline_top = 12
    offline_bottom = 18
    group_top = 20
    group_bottom = 23
    left = 78
    right = 94


def contactsBoxUpdate(contacts_data):
    # 清除页面
    for i in range(ContactsBox.left, ContactsBox.right + 1):
        for j in range(ContactsBox.online_top, ContactsBox.online_bottom):
            page[j][i] = " "
        for j in range(ContactsBox.offline_top, ContactsBox.offline_bottom):
            page[j][i] = " "
        for j in range(ContactsBox.group_top, ContactsBox.group_bottom):
            page[j][i] = " "
    online_div = page[ContactsBox.online_top:ContactsBox.online_bottom]
    offline_div = page[ContactsBox.offline_top:ContactsBox.offline_bottom]
    group_div = page[ContactsBox.group_top:ContactsBox.group_bottom]
    online_count = 0
    offline_count = 0
    group_count = 0
    for i in zip(contacts_data.keys(), contacts_data.values()):
        index = ContactsBox.left
        unread_num = i[1][0]
        if i[1][1] == "Friend":
            for j in i[0]:
                online_div[online_count][index] = j
                index = index + 1
            while index < ContactsBox.right:
                online_div[online_count][index] = " "
                index = index + 1
            if unread_num > 0:
                online_div[online_count][ContactsBox.right - 2] = getUtf8NumEmoji(unread_num)
            if unread_num > 10:
                online_div[online_count][ContactsBox.right - 1] = "+"
            online_count = online_count + 1
        elif i[1][1] == "Friend(Offline)":
            for j in i[0]:
                offline_div[offline_count][index] = j
                index = index + 1
            while index < ContactsBox.right:
                offline_div[offline_count][index] = " "
                index = index + 1
            if unread_num > 0:
                offline_div[offline_count][ContactsBox.right - 2] = getUtf8NumEmoji(unread_num)
            if unread_num > 10:
                offline_div[offline_count][ContactsBox.right - 1] = "+"
            offline_count = offline_count + 1
        else:
            for j in i[0]:
                group_div[group_count][index] = j
                index = index + 1
            while index < ContactsBox.right:
                group_div[group_count][index] = " "
                index = index + 1
            if unread_num > 0:
                group_div[group_count][ContactsBox.right - 2] = getUtf8NumEmoji(unread_num)
            if unread_num > 10:
                group_div[group_count][ContactsBox.right - 1] = "+"
            group_count = group_count + 1

    page[ContactsBox.online_top:ContactsBox.online_bottom] = online_div
    page[ContactsBox.offline_top:ContactsBox.offline_bottom] = offline_div
    page[ContactsBox.group_top:ContactsBox.group_bottom] = group_div


def show():
    lock.acquire()
    clear()
    for i in page:
        print("".join(i))
    lock.release()


def isChinese(ch):
    if '\u4e00' <= ch <= '\u9fff' or '\uFF01' <= ch <= '\uFF5E':
        return True
    return False


def clear():
    os.system('cls || clear')


def getUtf8NumEmoji(num):
    if num == 1:
        return '➀'
    elif num == 2:
        return '➁'
    elif num == 3:
        return '➂'
    elif num == 4:
        return '➃'
    elif num == 5:
        return '➄'
    elif num == 6:
        return '➅'
    elif num == 7:
        return '➆'
    elif num == 8:
        return '➇'
    elif num == 9:
        return '➈'
    elif num > 9:
        return '➉'