import os

from Utils import ReadFile, ReadData

record_path = r"MessageRecord/Data"


def getMessages(user_id, friend_id):
    path = os.path.join(record_path, user_id, friend_id + ".txt")
    path = os.path.abspath(path)
    return readLast20Lines(path)


def getUnreadNum(user_id, friend_id):
    path = os.path.join(record_path, user_id, "UnreadNum.txt")
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.open(path, os.O_CREAT, 0o666)
    data = ReadData.getData(path)
    if friend_id in data.keys():
        return int(data[friend_id][0])
    else:
        return 0


def setUnreadNum(user_id, friend_id, num):
    path = os.path.join(record_path, user_id, "UnreadNum.txt")
    path = os.path.abspath(path)
    data = ReadData.getData(path)
    data[friend_id] = num
    ReadData.setData(path, data)


# member_id 为 0 表示自己发出的消息 为 1 表示好友发来的消息 其他表示群友发来的消息
def addMessage(message, user_id, contact_id, member_id):
    path = os.path.join(record_path, user_id, contact_id + ".txt")
    path = os.path.abspath(path)
    file = open(path, 'a+')
    file.write(member_id + " " + str(getStringLength(message)) + " " + message + "\n")
    file.close()


def getStringLength(string):
    length = 0
    for i in string:
        if isChinese(i):
            length = length + 2
        else:
            length = length + 1
    return length


def isChinese(ch):
    if '\u4e00' <= ch <= '\u9fff' or '\uFF01' <= ch <= '\uFF5E':
        return True
    return False


def readLast20Lines(path):
    n = 1
    count = 0
    text = []
    while count < 20:
        data = ReadFile.readLineFromLast(path, n)
        if data is not None:
            string = data.decode("gbk").split(" ")
            string_len = int(string[1])
            count = count + int(string_len / 35) + 3
            if count >= 20:
                break
            text.append([string[0], string_len, " ".join(string[2:]).rstrip()])
            n = n + 1
        else:
            break
    return text[-1::-1]
