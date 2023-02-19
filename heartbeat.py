from srun import SrunClient
import socket

USERNAME = ''
PASSWD = ''

CHECK_SERVER = 'www.baidu.com'


def check_connect():
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect((CHECK_SERVER, 443))
        return True
    except Exception as e:
        print(e)
        return False


def check_online():
    if check_connect(): return
    srun_client = SrunClient(print_log=False)
    # Use this method frequently to check online is not suggested!
    # if srun_client.check_online(): return
    print('NOT ONLINE, TRY TO LOGIN!')
    srun_client.username = USERNAME
    srun_client.passwd = PASSWD
    srun_client.login()


if __name__ == "__main__":
    check_online()
    
#     import time
#     while 1:
#         check_online()
#         time.sleep(10)
