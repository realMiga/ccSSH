#!/usr/bin/env python3
# encoding: utf-8
import os

from Core.BaseClient import SSHClient
from DBManager.ShadowManager import ShadowManager


def show_main_menu():
    print('[*]ServerList:')
    print('(A)\t -->\t All')
    _tmp_color = '\033[01;3%dm'
    for _line in ss_list:
        _prompt = _tmp_color % (ss_list.index(_line) + 1)
        print("(%d)\t -->\t" % (ss_list.index(_line) + 1) + _prompt + _line + '\033[01;37m')
    print('(Q)\t -->\t Quit')


def show_task_menu():
    print('[*]Task List:')
    print('\033[00;32m(1)\t -->\t run command\033[01;37m')
    print('\033[00;33m(2)\t -->\t upload file\033[01;37m')
    print('\033[00;34m(3)\t -->\t download file\033[01;37m')
    print('\033[00;35m(0)\t -->\t cancel\033[01;37m')


def get_menu_choose():
    while True:
        _input_choose = input('[*]Choose Server (A/a, Q/q, %s): ' % (str(-1) + '~' + str(len(ss_list))))
        try:
            if _input_choose == 'A' or _input_choose == 'a':
                pass
            elif _input_choose == 'Q' or _input_choose == 'q':
                pass
            else:
                _input_choose = int(_input_choose)
                if _input_choose == 0:
                    print('[*]Choose Error: range must in A, Q, 1~%d' % len(ss_list))
                    continue
            return _input_choose
        except Exception as _e:
            print('[*]Choose Error:', _e)
            continue


def get_task_choose():
    while True:
        try:
            _input_choose = int(input('[*]Choose task to work 0~3: '))
            return _input_choose
        except Exception as _e:
            print('[*]Choose Error:', _e)
            continue


def exec_task(choose):
    if choose == 'Q' or choose == 'q':
        for _line in ss_list:
            client_map[_line].quit()
            print('[*]Close', _line)
        exit(0)
    elif choose == 'A' or choose == 'a':
        show_task_menu()
        task_choose = get_task_choose()
        if task_choose == 1:
            command = input("[*]Input Command: ")
            tmp_color = '\033[01;3%dm'
            for server in ss_list:
                prompt = tmp_color % (ss_list.index(server) + 1)
                print(prompt + '[*]%s result:' % server)
                _ret = client_map[server].run(command)
                for _line in _ret.get_out():
                    print(_line[:-1])
                print('Finish\n' if _ret.suc else 'Fail\n', '\033[01;37m')
        elif task_choose == 2:
            local_path = input("[*]Upload local file relative path: ")
            remote_path = input("[*]Upload path: ")
            tmp_color = '\033[01;3%dm'
            for server in ss_list:
                prompt = tmp_color % (ss_list.index(server) + 1)
                print(prompt + '[*]%s result:' % server)
                _ret = client_map[server].upload(local_path, remote_path)
                if _ret.suc:
                    print('\033[00;32m[+]Upload success')
                else:
                    print('\033[00;31m[!]Upload fail(%s)' % _ret.std_err)
                print('\033[01;37m')
        elif task_choose == 3:
            remote_file = input("[*]Remote file relative path: ")
            tmp_color = '\033[01;3%dm'
            for server in ss_list:
                if not os.path.exists(server):
                    os.mkdir(server)
                local_path = os.path.join(os.getcwd(), server)
                prompt = tmp_color % (ss_list.index(server) + 1)
                print(prompt + '[*]%s result:' % server)
                _ret = client_map[server].download(remote_file, local_path)
                if _ret.suc:
                    print('\033[00;32m[+]Download success')
                else:
                    print('\033[00;31m[!]Download fail(%s)' % str(_ret.std_err))
                print('\033[01;37m')
        elif task_choose == 0:
            return
    elif (input_choose - 1) < len(ss_list):
        show_task_menu()
        task_choose = get_task_choose()

        server = ss_list[input_choose - 1]
        prompt = '\033[01;3%dm' % (ss_list.index(server) + 1)
        _client = client_map[server]

        if task_choose == 1:
            command = input("[*]Input Command: ")
            print(prompt + '[*]%s result:' % server)
            _ret = _client.run(command)
            for _line in _ret.get_out():
                print(_line[:-1])
            print('Finish\n' if _ret.suc else 'Fail\n', '\033[01;37m')
        elif task_choose == 2:
            local_path = input("[*]Upload local file relative path: ")
            remote_path = input("[*]Upload path: ")
            print(prompt + '[*]%s result:' % server)
            _ret = client_map[server].upload(local_path, remote_path)
            if _ret.suc:
                print('\033[00;32m[+]Upload success')
            else:
                print('\033[00;31m[!]Upload fail(%s)' % _ret.std_err)
            print('\033[01;37m')
        elif task_choose == 3:
            remote_file = input("[*]Remote file relative path: ")
            if not os.path.exists(server):
                os.mkdir(server)
            local_path = os.path.join(os.getcwd(), server)
            print(prompt + '[*]%s result:' % server)
            _ret = _client.download(remote_file, local_path)
            if _ret.suc:
                print('\033[00;32m[+]Download success')
            else:
                print('\033[00;31m[!]Download fail(%s)' % str(_ret.std_err))
            print('\033[01;37m')
        elif task_choose == 0:
            return
    else:
        print('[*]Has not this task')


server_list = ShadowManager.get_all_server().Result
client_map = {}
for line in server_list:
    try:
        client = SSHClient(line)
        client.connect(reconnect=5)
        client_map[line['f_name']] = client
        print('\033[01;37mconnected', line['f_name'])
    except Exception as e:
        print(e)
        print(line['f_name'])
        continue

ss_list = list(client_map.keys())


while 1:
    show_main_menu()
    input_choose = get_menu_choose()
    exec_task(input_choose)



