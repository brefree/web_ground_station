import socket, os, json, androidhelper

host_path = r'Z:\\'
hostport = ('192.168.199.230', 5556)
# hostport = ('182.61.48.178', 5556)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP socket
# s.bind(hostport)
s.connect(hostport)  # 链接套接字

while True:
    user_input = input('001>>>:').strip()
    if not len(user_input):
        continue
    if user_input == 'go':
        Droid = androidhelper.Android()
        location = Droid.getLastKnownLocation().result
        location = location.get('network', location.get('gps'))
        s_data = json.dumps(location)
        s.send(s_data.encode())
    elif user_input == 'quit':
        s.send(user_input.encode())
        s.close()
        break
    server_reply = s.recv(1024)  # 接收套接字数据
    if not server_reply:
        break
    reply_data = server_reply.decode()
    print(reply_data)
