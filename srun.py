import time

if bytes is str: input = raw_input

import urequests as requests

def dict2list( dict_ , sep ):
    _list = list()
    for item_name in dict_.keys():
        _list.append( '%s%s%s'%( item_name , sep  , dict_.get( item_name ) )  )
    return _list

def data2formurlencoded( data ):
    return '&'.join( dict2list(data, "=") )

def get_func(url, *args, **kwargs):
    resp = requests.get(url, *args, **kwargs)
    return resp.text

def post_func(url, data, headers , *args, **kwargs):
    if data is not None:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        data = data2formurlencoded( data )
    resp = requests.post(url, *args, data=data, headers=headers, **kwargs)
    return resp.text

def time2date(timestamp):
    time_arry = time.localtime(int(timestamp))
    return '%02d-%02d-%02d %02d:%02d:%02d'%( time_arry[0:6] )


def humanable_bytes(num_byte):
    num_byte = float(num_byte)
    num_GB, num_MB, num_KB = 0, 0, 0
    if num_byte >= 1024**3:
        num_GB = num_byte // (1024**3)
        num_byte -= num_GB * (1024**3)
    if num_byte >= 1024**2:
        num_MB = num_byte // (1024**2)
        num_byte -= num_MB * (1024**2)
    if num_byte >= 1024:
        num_KB = num_byte // 1024
        num_byte -= num_KB * 1024
    return '{} GB {} MB {} KB {} B'.format(num_GB, num_MB, num_KB, num_byte)


def humanable_bytes2(num_byte):
    num_byte = float(num_byte)
    if num_byte >= 1024**3:
        return '{:.2f} GB'.format(num_byte/(1024**3))
    elif num_byte >= 1024**2:
        return '{:.2f} MB'.format(num_byte/(1024**2))
    elif num_byte >= 1024**1:
        return '{:.2f} KB'.format(num_byte/(1024**1))


class SrunClient:
    
    name = 'CUGB'

    login_url = 'http://{}/cgi-bin/srun_portal'
    online_url = 'http://{}/cgi-bin/rad_user_info'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    def __init__(self, username=None, passwd=None, print_log=True , srun_ip='202.204.105.195'):
        self.username = username
        self.passwd = passwd
        self.print_log = print_log
        self.online_info = dict()
        self.srun_ip = srun_ip
        self.check_online()

    def _encrypt(self, passwd):
        column_key = [0,0,'d','c','j','i','h','g']
        row_key = [
            ['6','7','8','9',':',';','<','=','>','?','@','A','B','C','D','E'],
            ['?','>','A','@','C','B','E','D','7','6','9','8',';',':','=','<'],
            ['>','?','@','A','B','C','D','E','6','7','8','9',':',';','<','='],
            ['=','<',';',':','9','8','7','6','E','D','C','B','A','@','?','>'],
            ['<','=',':',';','8','9','6','7','D','E','B','C','@','A','>','?'],
            [';',':','=','<','7','6','9','8','C','B','E','D','?','>','A','@'],
            [':',';','<','=','6','7','8','9','B','C','D','E','>','?','@','A'],
            ['9','8','7','6','=','<',';',':','A','@','?','>','E','D','B','C'],
            ['8','9','6','7','<','=',':',';','@','A','>','?','D','E','B','C'],
            ['7','6','8','9',';',':','=','<','?','>','A','@','C','B','D','E'],
        ]
        encrypt_passwd = ''
        for idx, c in enumerate(passwd):
            char_c = column_key[ord(c) >> 4]
            char_r = row_key[idx%10][ord(c) & 0xf]
            if idx%2:
                encrypt_passwd += char_c + char_r
            else:
                encrypt_passwd += char_r + char_c
        return encrypt_passwd
    
    def _log(self, msg):
        if self.print_log:
            print('[SrunClient {}] {}'.format(self.name, msg))

    def check_online(self):
        resp_text = get_func(self.online_url.format( self.srun_ip ), headers=self.headers)
        if 'not_online' in resp_text:
            self._log('###*** NOT ONLINE! ***###')
            return False
        try:
            items = resp_text.split(',')
            self.online_info = {
                'online':True, 'username':items[0], 
                'login_time':items[1], 'now_time':items[2], 
                'used_bytes':items[6], 'used_second':items[7], 
                'ip':items[8], 'balance':items[11], 
                'auth_server_version':items[21]
                }
            return True
        except Exception as e:
            print(resp_text)
            print('Catch `Status Internal Server Error`? The request is frequent!')
            print(e)
    
    def show_online(self):
        if not self.check_online(): return
        self._log('###*** ONLINE INFORMATION! ***###')
        header = '================== ONLIN INFORMATION =================='
        print(header)
        print('Username: {}'.format(self.online_info['username']))
        print('Login time: {}'.format(time2date(self.online_info['login_time'])))
        print('Now time: {}'.format(time2date(self.online_info['now_time'])))
        print('Used data: {}'.format(humanable_bytes(self.online_info['used_bytes'])))
        print('Ip: {}'.format(self.online_info['ip']))
        print('Balance: {}'.format(self.online_info['balance']))
        print('=' * len(header))

    def login(self):
        if self.check_online():
            self._log('###*** ALREADY ONLINE! ***###')
            return True
        if not self.username or not self.passwd:
            self._log('###*** LOGIN FAILED! (username or passwd is None) ***###')
            self._log('username and passwd are required! (check username and passwd)')
            return False
        encrypt_passwd = self._encrypt(self.passwd)
        payload = {
            'action': 'login',
            'username': self.username,
            'password': encrypt_passwd,
            'type': 2, 'n': 117,
            'drop': 0, 'pop': 0,
            'mbytes': 0, 'minutes': 0,
            'ac_id': 1
            }
        resp_text = post_func(self.login_url.format(self.srun_ip), data=payload, headers=self.headers)
        if 'login_ok' in resp_text:
            self._log('###*** LOGIN SUCCESS! ***###')
            self._log(resp_text)
            # self.show_online()
            return True
        elif 'login_error' in resp_text:
            self._log('###*** LOGIN FAILED! (login error)***###')
            self._log(resp_text)
            return False
        else:
            self._log('###*** LOGIN FAILED! (unknown error) ***###')
            self._log(resp_text)
            return False

    def logout(self):
        if not self.check_online(): return True
        payload = {
            'action': 'logout',
            'ac_id': 1,
            'username': self.online_info['username'],
            'type': 2
            }
        resp_text = post_func(self.login_url.format(self.srun_ip) , data=payload, headers=self.headers)
        if 'logout_ok' in resp_text:
            self._log('###*** LOGOUT SUCCESS! ***###')
            return True
        elif 'login_error' in resp_text:
            self._log('###*** LOGOUT FAILED! (login error) ***###')
            self._log(resp_text)
            return False
        else:
            self._log('###*** LOGOUT FAILED! (unknown error) ***###')
            self._log(resp_text)
            return False

    def set_srun_ip(self , srun_ip):
        self.srun_ip = srun_ip

def show_commands():
    wellcome = '############### Wellcome to Srun Client ###############'
    print(wellcome)
    print('[1]: show online information')
    print('[2]: set username and passwd')
    print('[3]: login')
    print('[4]: logout')
    print('[h]: show this messages')
    print('[q]: quit')
    print('#' * len(wellcome))


if __name__ == "__main__":
    srun_client = SrunClient()
    show_commands()
    srun_client.show_online()
    command = '_'
    while command != 'q':
        command = input('>')
        if command == '1':
            srun_client.show_online()
        elif command == '2':
            srun_client.username = input('username: ')
            srun_client.passwd = input('passwd: ')
        elif command == '3':
            srun_client.login()
        elif command == '4':
            srun_client.logout()
        elif command == 'h':
            show_commands()
        elif command == 'q':
            print('bye!')
        else:
            print('unknown command!')
