# Serial_Server

# 简介

`Serial_Server` 是 [Serial_Client](https://github.com/Elinpf/Serial_Client)的服务器端。

提供了房间功能，方便远端工程师在SSH的方式登录后通过选择房间号进入对应的终端。

与`Serial_Client` 端的注册端口默认为`2200`, 远端SSH监听端口为`2300`。

# 安装方法

```
git clone https://github.com/Elinpf/Serial_Server.git
```

# 使用方法

```
cd Serial_Server
python3 ./start.py
```

# TODO