# simpleDemo
python-控制QQ回复消息

安装pywin32
> pip install pywin32

安装ZMQ
> pip install pyzmq


控制端 + 服务端 + 客户端

控制端设置暗号后， 每次发送的信息将被服务端转发到 处于运行状态中的客户端;
服务端用于转发message;
客户端设置窗体名称和暗号后, 接收来自控制端的message(同一暗号的控制端才可), 然后打开QQ, 发送message.
