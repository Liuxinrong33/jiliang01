import socket


"""
课 2 上课用品

本次上课的主要内容有
0, 请注意代码的格式和规范
1, 规范化生成响应
2, HTTP 头
3, 几个常用 HTML 标签及其用法
4, 参数传递的两种方式
"""


def log(*args, **kwargs):
    """
    用这个 log 替代 print
    """
    print('log', *args, **kwargs)
    pass


def html_content(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def route_index():
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 gua\r\nContent-Type: text/html\r\n'
    body = html_content('app.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# def route_message():
#     header = 'HTTP/1.1 200 gua\r\nContent-Type: text/html\r\n'
#     body = html_content('html_basic.html')
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


"""
POST /postgua HTTP/1.1
Host: localhost:3000
Content-Length: 24
Content-Type: application/x-www-form-urlencoded

message=hello&author=gua
"""


# def route_message_add():
#     # 这个函数现在什么都干不了
#     # 因为你没办法获取到浏览器传过来的数据
#     form = dict(
#         message='hello',
#         author='gua',
#     )
#     header = 'HTTP/1.1 200 gua\r\nContent-Type: text/html\r\n'
#     body = html_content('html_basic.html')
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


def route_css():
    """
    css的处理函数, 读取css并生成响应返回
    """
    header = 'HTTP/1.1 200 gua\r\nContent-Type: text/css\r\n'
    body = html_content('sty01.css')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/jiliang': route_index,
        '/sty01.css': route_css,
        # '/message': route_message,
        # '/message/add': route_message_add,
    }
    # get 函数是字典的函数
    # 第二个参数是默认值
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket() as gua:
        gua.bind((host, port))
        # 监听 接受 读取请求数据 解码成字符串
        gua.listen(5)
        # 无限循环来处理请求
        while True:
            connection, address = gua.accept()
            # 这里只读取了 1024 字节的内容, 应该用一个循环全部读取
            # 但现在我们不用考虑那么多
            request = connection.recv(1024)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                # 因为 chrome 会发送空请求导致 split 得到空 list
                # 所以这里用 try 防止程序崩溃
                path = request.split()[1]
                # 用 response_for_path 函数来得到 path 对应的响应内容
                response = response_for_path(path)
                # 把响应发送给客户端
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            # 处理完请求, 关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    # 如果不了解 **kwargs 的用法, 群里问或者看书/搜索 关键字参数
    run(**config)
