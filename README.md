# SmartChat-for-Linux: 嵌入式Linux系统下的智能聊天室

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)](https://github.com/SCIR-HI/Med-ChatGLM/blob/main/LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-3810/)

本项目主要是基于“嵌入式Linux系统下的局域网聊天软件设计”的课题要求，组队完成的项目。

系统主要由**客户端**和**服务器**组成。

* **客户端**由用户使用，负责与用户的交互。用户可以使用客户端登录聊天室进行聊天。
* **服务器**主要负责用户消息的处理和转发，所有用户消息必须经由服务器发送至其他用户。

## A Quick Start

1. 首先安装依赖包，python环境建议3.8+

```
pip install -r requirements.txt
```

修改文件：

* 修改Server目录下demo.py文件下main()函数中的host、port
* 修改Client目录下data.properties文件相应的serv_host、serv_port、local_host、local_port

本地ip地址查找：

* Linux通过ifconfig命令来查找ip地址
* Windows通过ipconfig命令来查找ip地址

运行Server目录下的demo.py文件

```
python Server/demo.py
```

运行Client目录下的demo.py文件

```
python Client/demo.py
```

执行相应指令

## 指令

以下是实现的各个指令：

|      指令      |      功能      |     指令     |    功能    |
| :------------: | :------------: | :----------: | :--------: |
|   `/help`   |      帮助      | `/confirm` |  同意通知  |
| `/register` |      注册      | `/refuse` |  拒绝通知  |
|   `/login`   |      登录      |   `/ban`   | 群成员禁言 |
|  `/logout`  |    退出登录    |  `/unban`  |   解禁言   |
| `/changepwd` |    修改密码    |  `/kick`  | 踢出群成员 |
|    `/add`    | 添加好友或群聊 |  `/chat`  |    聊天    |
|    `/del`    | 删除好友或群聊 |   `/end`   |  结束聊天  |
|  `/chatgpt`  | 与ChatGPT对话 |  `/exit`  |    退出    |

## 项目要求

1. 采用Linux系统下的C、C++或Python语言设计。
2. 服务器和客户端使用**TCP协议**进行通信，同时使用特定的端口号。服务器有着固定的IP地址，每个客户端有不同的IP地址。
3. 首先需要保证服务器正在运行中，才可以处理客户的消息。
4. 用户通过客户端的界面进行操作，客户端与服务器进行通信，将要发送的聊天消息和相关信息使用Socket发送给服务器。
5. 服务器按照消息的发送设置（群聊、私聊等）将消息发送给特定的用户。

## 常见问题

1. Q: 两台虚拟机未能ping通

   A: 虚拟机网络适配器改为桥接模式，参考此文档进行设置：[两台虚拟机如何ping通](https://blog.csdn.net/weixin_54763080/article/details/128356861)。
2. Q: 运行结束后重新启动发现端口被占用

   A: 重新使用ifconfig(ipconfig)获取ip地址，修改对应文件重新运行。

## 免责声明

本项目相关资源仅供学术研究之用，严禁用于商业用途。使用涉及第三方代码的部分时，请严格遵循相应的开源协议。模型生成的内容受模型因素影响，本项目无法对其准确性作出保证。该项目设计使用了开源技术和第三方库，但无法对这些技术和库的质量、功能和安全性进行担保。请在使用前仔细阅读相关文档，并自行评估其适用性和安全性。该项目设计涉及网络通信和数据传输，但无法对传输过程中的安全性和完整性做出绝对保证。在实际使用中，请确保采取适当的安全措施，并自行承担相关风险。对于模型输出的任何内容，本项目不承担任何法律责任，亦不对因使用相关资源和输出结果而可能产生的任何损失承担责任。

## Citation

如果你使用了本项目的数据或者代码，请声明引用

```
@misc{SmartChat-for-Linux,
  author={HuangChong Xuan,ZhaoJian Hao,TangDing Jun,LuoChao Wen,KeHao Peng},
  title = {SmartChat-for-Linux: 嵌入式Linux系统下的智能聊天室},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ustbHCX/SmartChat-for-Linux}},
}
```
