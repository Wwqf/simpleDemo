import zmq
import json
import threading

controllerGroup = set()


class Rec(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        context = zmq.Context()
        self.controllerSocket = context.socket(zmq.REP)
        self.controllerSocket.bind("tcp://*:5550")

        self.clientSocket = context.socket(zmq.PUB)
        self.clientSocket.bind("tcp://*:5551")

    def run(self):
        print('开启监听请求...')
        while True:
            self.recController()

    def recController(self):
        recJson = self.controllerSocket.recv_json()
        print('接收来自controller端的数据: ', recJson)

        if recJson['src'] == 'verify':
            # 验证班级信息
            self.verifyClassInfo(recJson)
        elif recJson['src'] == 'message':
            # 发送消息
            self.broadcastMessage(recJson)

    def verifyClassInfo(self, recJson):
        if recJson['verify'] in controllerGroup:
            self.controllerSocket.send_json({
                'id': 0
            })

        self.controllerSocket.send_json({
            'id': recJson['verify']
        })
        controllerGroup.add(recJson['verify'])

        print('当前订阅班级有: ', controllerGroup)

    def broadcastMessage(self, recJson):
        if recJson['mode'] == 'c':
            # 向所有订阅此班级的client发送msg
            self.clientSocket.send_string('%i,%s' % (recJson['id'], recJson['msg']))

            # 回复状态
            self.controllerSocket.send_json({
                'status': 0
            })
        elif recJson['mode'] == 'p':
            pass


def main():
    rec = Rec()
    rec.start()


if __name__ == '__main__':
    main()
