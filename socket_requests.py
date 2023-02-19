import socket


def dict2list( dict_ , sep ):
    _list = list()
    for item_name in dict_.keys():
        _list.append( '%s%s%s'%( item_name , sep  , dict_.get( item_name ) )  )
    return _list

def post(domain, port, path, data, headers):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((domain, port))

    sock.send('POST'.encode())
    sock.send(' '.encode())
    sock.send(path.encode())
    sock.send(' HTTP/1.1\r\n'.encode())

    data_list = dict2list( data , "=" )

    data_str = '&'.join(data_list)

    headers['Host'] = domain
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Content-Length'] = str(len(data_str))
    headers['Connection'] = 'close'

    sock.send('\r\n'.join(dict2list( headers , ": " )).encode())

    sock.send('\r\n\r\n'.encode())
    sock.send(str(data_str).encode())

    sock.send('\r\n'.encode())
    response = b''
    # 接收返回的数据
    rec = sock.recv(1024)
    while rec:
        response += rec
        rec = sock.recv(1024)

    content = response.decode()
    text = content.split('\r\n\r\n')[1]
    sock.close()
    return text


def get(domain, port, path, headers):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((domain, port))

    sock.send('GET'.encode())
    sock.send(' '.encode())
    sock.send(path.encode())
    sock.send(' HTTP/1.1\r\n'.encode())

    headers['Host'] = domain
    headers['Connection'] = 'close'

    sock.send('\r\n'.join(dict2list(headers, ": ")).encode())

    # sock.send('\r\nConnection: close\r\n\r\n'.encode())
    sock.send('\r\n\r\n'.encode())

    response = b''

    sock.settimeout(2)
    rec = sock.recv(1)
    while rec:
        response += rec
        rec = sock.recv(1)

    content = response.decode()

    text = content.split('\r\n\r\n')[1]
    sock.close()
    return text


