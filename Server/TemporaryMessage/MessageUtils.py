import os


offline_message_path = r"TemporaryMessage/Data"


def getOfflineMessagesById(user_id):
    path = os.path.join(offline_message_path, user_id + ".txt")
    path = os.path.abspath(path)
    file = open(path, 'r')
    offline_messages = file.readlines()
    file.close()
    return offline_messages


def addOfflineMessageById(user_id, message):
    path = os.path.join(offline_message_path, user_id + ".txt")
    path = os.path.abspath(path)
    file = open(path, 'a')
    file.write(str(message, 'utf8')  + "\n")
    file.close()


def clearOfflineMessageById(user_id):
    path = os.path.join(offline_message_path, user_id + ".txt")
    path = os.path.abspath(path)
    file = open(path, 'w')
    file.close()
