from srun import SrunClient
import socket

USERNAME = ''
PASSWD = ''
SRUN_IP = '202.204.105.195'
CHECK_SERVER = 'www.baidu.com'


def check_online():
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect((CHECK_SERVER, 443))
        return True
    except Exception as e:
        print(e)
        return False


def try_login( username, passwd, srun_ip ):
    srun_client = SrunClient( username=username, passwd=passwd, srun_ip=srun_ip , print_log=False)
    # Use this method frequently to check online is not suggested!
    # if srun_client.check_online(): return
    srun_client.username = USERNAME
    srun_client.passwd = PASSWD
    return srun_client.login()


def main():
    if check_online(): return
    print('NOT ONLINE, TRY TO LOGIN!')
    if not try_login(USERNAME, PASSWD, SRUN_IP):
        raise Exception("LOGIN FAILED!")


if __name__ == "__main__":
    main()
    
#     import time
#     while 1:
#         main()
#         time.sleep(10)
