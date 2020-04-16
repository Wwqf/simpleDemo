import zmq
import win32gui
import win32con
import win32clipboard as w

context = zmq.Context()
socket = context.socket(zmq.SUB)

addr = "localhost"
socket.connect("tcp://" + addr + ":5551")

winName = input("请输入窗体名称: ")

signal = input("请输入暗号: ")
socket.setsockopt_string(zmq.SUBSCRIBE, signal)


def sendMsg(msg):
    # 将测试消息复制到剪切板中
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, msg)
    w.CloseClipboard()
    # 获取窗口句柄
    handle = win32gui.FindWindow(None, winName)
    # while 1==1:
    if 1 == 1:
        # 填充消息
        win32gui.SendMessage(handle, 770, 0, 0)
        # 回车发送消息
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)

while True:
    recStr = socket.recv_string()
    print(recStr)

    msg = recStr.split(',')[1]
    sendMsg(msg=msg)
