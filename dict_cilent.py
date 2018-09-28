#!/usr/bin/python3
# coding=utf-8

from socket import *
import sys
import getpass


def main():
    if len(sys.argv) < 3:
        print('argv is erro')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print(e)
        return
    while True:
        print('''
            =========Welcome========
            --1.注册  2.登录  3.退出--
            ========================
            ''')
        try:
            cmd = int(input('输入选项>>'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1, 2, 3]:
            print('请输入正确选项')
            sys.stdin.flush()  # 清除标准输入
        elif cmd == 1:
            r = do_register(s)
            if r == 0:
                print('注册成功')
                # loginin(s, name)
            elif r == 1:
                print('用户已存在')
            else:
                print('注册失败')
        elif cmd == 2:
            name = do_login(s)
            if name:
                print('登录成功')
                login(s, name)
            else:
                print('用户名或密码错误')
        elif cmd == 3:
            s.send(b'E')
            sys.exit('谢谢使用！！！')


def do_register(s):
    while True:
        name = input('输入注册用户名：')
        password = getpass.getpass('输入密码：')
        password1 = getpass.getpass('确认密码：')
        if (' ' in name) or (' ' in password):
            print('用户名和密码不允许有空格')
            continue
        if password != password1:
            print('两次输入密码不一致')
            continue
        msg = 'R {} {}'.format(name, password)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return 0
        elif data == 'EXISTS':
            return 1
        else:
            return 2


def do_login(s):
    while True:
        name = input('输入登录用户名：')
        password = getpass.getpass('输入密码：')
        msg = 'L {} {}'.format(name, password)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return name
        else:
            return


def login(s, name):
    while True:
        print('''
        ========查询界面=========
         1查询  2历史记录  3退出 
        ========================
        ''')
        try:
            cmd = int(input('输入选项>>'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1, 2, 3]:
            print('请输入正确选项')
            sys.stdin.flush()  # 清除标准输入
            continue
        elif cmd == 1:
            do_query(s, name)
        elif cmd == 2:
            do_hist(s, name)
        elif cmd == 3:
            return


def do_query(s, name):
    while True:
        word = input('输入查询单词：')
        if word == '##':
            break
        msg = 'Q {} {}'.format(name, word)
        s.send(msg.encode())
        data = s.recv(128).decode()
        print(data)
        if data == 'OK':
            data = s.recv(2048).decode()
            print(data)
        else:
            print('单词不存在')


def do_hist(s, name):
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print('没有历史记录')


if __name__ == '__main__':
    main()
