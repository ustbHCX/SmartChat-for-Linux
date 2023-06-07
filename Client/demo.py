import os
import signal
import sys
import time
from threading import Thread

from Net import TCP, NetUtils
from Utils import Command
from Cache import CacheUtils


def getInput():
    print("Welcome! Please input /help to get helps.")
    while True:
        # 1.获取输入
        i = input()

        # 2.检测是否输入为空
        if i.lstrip() == "":
            continue

        # 3.检测当前输入是否为指令
        elif i.lstrip()[0] == '/':
            # 拆分指令
            tmp = i.split(' ')
            cmd = tmp[0]
            params = tmp[1:]

            # 检测退出指令
            if cmd == '/exit':
                Command.execute("/logout".split(' ')[0], "/logout".split(' ')[1:])
                sys.exit()
            else:
                Command.execute(cmd, params)

        # 4.默认输入为聊天内容
        else:
            NetUtils.sendMessage(i)

        # 5.延时
        time.sleep(0.1)


def main():
    # 1.绑定线程
    thread_listen = Thread(target=TCP.listen)
    thread_get_input = Thread(target=getInput)

    # 2.启动线程
    thread_listen.start()
    thread_get_input.start()

    # 3.捕捉程序关闭信号
    if os.name == "posix":
        signal.signal(signal.SIGHUP | signal.SIGINT | signal.SIGKILL, CacheUtils.getCurrentUser().logout)
    elif os.name == "nt":
        import win32api
        import win32con
        win32api.SetConsoleCtrlHandler(lambda event: CacheUtils.getCurrentUser().logout()
        if event in [win32con.CTRL_C_EVENT, win32con.CTRL_LOGOFF_EVENT,
                     win32con.CTRL_BREAK_EVENT, win32con.CTRL_SHUTDOWN_EVENT,
                     win32con.CTRL_CLOSE_EVENT] else None, 1)

    # 等待子线程结束
    thread_get_input.join()


main()
