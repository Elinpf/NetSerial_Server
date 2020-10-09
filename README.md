# Serial_Server

# 简介

`Serial_Server` 是 [Serial_Client](https://github.com/Elinpf/NetSerial_Client)的服务器端。

提供了房间功能，方便远端工程师在SSH的方式登录后通过选择房间号进入对应的终端。

与`Serial_Client` 端的注册端口默认为`2200`, 远端SSH监听端口为`2300`。

# 安装方法

```
git clone https://github.com/Elinpf/NetSerial_Server.git
```

# 配置

打开`custom.json`文件，修改所需配置。

- "SSH_SERVER_USERNAME": "bar"   # 登录服务器的用户名
- "SSH_SERVER_PASSWORD": "foo"   # 登录服务器的密码 
- "SSH_SERVER_LISTENING_IP": "127.0.0.1"  # 服务器对应的IP地址
- "SSH_SERVER_LISTENING_CLIENT_PORT": 2200  # 对Client端的监听端口
- "SSH_SERVER_LISTENING_TERMINIAL_PORT": 2300  # 对使用者的端口
- "SSH_SERVER_RSA_EKY": "server_rsa"  # 私钥文件目录，通常使用 `ssh-keygen`生成

# 使用方法

```
cd Serial_Server
python3 ./start.py
```

# TODO