import socket, os, json

host_path = r'Z:\\'
hostport = ('127.0.0.1', 5556)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP socket
# s.bind(hostport)
s.connect(hostport)  # 链接套接字

while True:
    # user_input = '你好,我是002'
    user_input = input('002>>>:').strip()
    s.send(user_input.encode())  # 发送数据到套接字
    if not len(user_input): continue
    server_reply = s.recv(1024)  # 接收套接字数据
    if not server_reply: break
    lsdata = server_reply.decode()
    print(lsdata)
    s_data = {'1': '12', '2': '23'}
    s_json = json.dumps(s_data)
    s.send(s_json.encode())
    if user_input == 'quit':
        s.close()
        break
