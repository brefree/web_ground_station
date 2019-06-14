from datetime import datetime
from socketserver import ThreadingTCPServer, StreamRequestHandler
import os, json

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uav02.settings")  # project_name 项目名称
django.setup()

from map.models import Uav, RealPoint

host_path = os.getcwd()


class MyHandler(StreamRequestHandler):

    def handle(self):
        print('clientaddr:', self.client_address, datetime.now())
        self.uav = Uav.objects.filter(ip=self.client_address[0]).first()
        if self.uav:
            self.uav.status = 1
            self.uav.save()
            print('飞机已经上线')
        else:
            print('此飞机不存在')
        while True:
            try:
                data = self.request.recv(1024)
                action = data.decode()
                if action == 'quit':
                    self.uav.status = 2
                    self.uav.save()
                    print('链接已关闭')
                    break
                print(action)
                real_data = json.loads(action)
                print(real_data, type(real_data))
                self.request.send('收到'.encode())
                if action == 'quit':
                    self.uav.status = 2
                    self.uav.save()
                    print('链接已关闭')
                    break
                RealPoint(uav_id=self.uav.id, real_altitude=real_data['altitude'], real_latitude=real_data['latitude'],
                          real_longitude=real_data['longitude'], real_vs=real_data['speed']).save()
            except Exception:
                self.uav.status = 2
                self.uav.save()
                print('飞机异常断线')
                break


if __name__ == "__main__":
    hostprot = ('0.0.0.0', 5556)
    server = ThreadingTCPServer(hostprot, MyHandler)
    print('connection to who...')
    server.serve_forever()
