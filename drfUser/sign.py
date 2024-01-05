from datetime import datetime
from blinker import Namespace
from drfUser.models import Loginlogs

# 创建一个命名空间
namespace = Namespace()
# 定义一个登录信号
login_sign = namespace.signal('login')
import socket


def get_local_ip():
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接一个外部服务器
        s.connect(("8.8.8.8", 80))
        # 获取本地IP地址
        ip = s.getsockname()[0]
        # 关闭socket连接
        s.close()
        return ip
    except socket.error:
        return "获取IP失败"


def login_log(sender, username):  # 第一个参数必须是sender
    ip = get_local_ip()
    login_time = datetime.now()
    recode_log = Loginlogs(username=username, ip=ip, login_time=login_time)
    recode_log.save()


login_sign.connect(login_log)  # 监听信号要传入一个函数，用于发送信号后执行
