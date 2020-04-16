import zmq
import threading
import json

# 控制端 端口(5550):
#   1. 设置 班级
#   2. 向班级内发送信息
#   3. 指定人选发送信息

'''
    第一次验证Json:
        {
            'src': 'verify',
            'verify': 'signal'
        }
        
        获取分配的id, 如果没有id或着id为0, 则异常, 视为连接失败.
    
    发送信息Json:
        {
            'src': 'message'
            'id': id,
            'mode': 'p|c',
            'msg': msg
        }
        
        controller的id, 方式为向全班发送或是个人集体, 返回0为正常, 其他都为异常代码
'''


class ConnectServer:
    def __init__(self):
        # signal跟id是一回事, 在原来的版本中使用的classname, 后更改的是signal
        self.signal = None
        self.id = None
        self.context = None
        self.socket = None

        self.addr = 'localhost'

    def initSignal(self):
        self.signal = int(input('请输入暗号: '))

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://" + self.addr + ":5550")
        print("开启连接服务器, 验证身份...")

        self.socket.send_json({
            'src': 'verify',
            'verify': self.signal
        })
        recMsg = self.socket.recv_json()
        self.recVerifyId(recMsg)

    def recVerifyId(self, recMsg):
        if 'id' in recMsg:
            self.id = recMsg['id']
            if self.id == 0:
                print('验证身份错误, 请重试!')
                # Todo error termination
            else:
                print('验证身份成功')
        else:
            print('验证身份失败...')
            # Todo error termination


class MonitorConsole(threading.Thread):
    # 监听控制台
    def __init__(self, connectServerInstance):
        threading.Thread.__init__(self)
        self.connectServer = connectServerInstance

    def run(self):
        print('开启监听控制台... ')
        while True:
            command = input("$ ")
            exitStatus = self.processCommand(command)
            if exitStatus:
                break

    def processCommand(self, command):
        if command.__eq__(''):
            return False

        if command.__eq__('exit'):
            return True

        data = command.split('-')
        if len(data) == 1:
            # 向班级发送
            self.connectServer.socket.send_json({
                'src': 'message',
                'id': self.connectServer.id,
                'mode': 'c',
                'msg': data[0]
            })

            # Todo 接收返回信息
            recMsg = self.connectServer.socket.recv_json()
        elif len(data) == 2:
            # sample: -p Liu, Yang msg
            data = data[1].split(' ')
            print(data)

            obj = []
            for item in range(1, len(data) - 1):
                # 检查是否有 ,
                array = data[item].split(',')
                if len(array) != 1:
                    # 分割
                    for o in array:
                        if o != '':
                            obj.append(o)
                    pass
                else:
                    # 只有一个对象
                    obj.append(data[item])

            self.connectServer.socket.send_json({
                'src': 'message',
                'id': self.connectServer.id,
                'mode': data[0],
                'obj': obj,
                'msg': data[-1]
            })
            # Todo 接收返回信息
            recMsg = self.connectServer.socket.recv_json()
        return False


def main():
    connectServer = ConnectServer()
    connectServer.initSignal()
    connectServer.connect()

    monitorConsole = MonitorConsole(connectServer)
    monitorConsole.start()


if __name__ == '__main__':
    main()
