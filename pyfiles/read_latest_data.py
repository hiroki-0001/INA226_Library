#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fcntl
import log_data_pb2

#ログを保存するファイル,シリアライズされたバイナリが保存されている
log_file_path = '/var/tmp/log_voltage_and_current.dat'
#ログを保存するファイル用のロックファイル
lock_log_file_path = '/var/tmp/lock_voltage_and_current.lock'


def main():
    #排他ロックの取得
    print('read log data...\n This program may need some time. Please wait a moment.')
    lock_file = open(lock_log_file_path, 'r+')
    fcntl.lockf(lock_file, fcntl.LOCK_EX)

    # ログファイルの読み込み
    try:
        log_file = open(log_file_path, 'r')
        log_data_lines = log_file.readlines()
        log_file.close()
    finally:
        #排他ロックの解放
        fcntl.lockf(lock_file, fcntl.LOCK_UN)
    

    with open('file.txt', 'r') as f:
        last_line = f.readlines()[-1]
    fcntl.lockf(lock_file, fcntl.LOCK_UN)
    log_data = log_data_pb2.PowerLog()
    log_data.ParseFromString(bytes.fromhex(last_line))
    print(log_data)
    
if __name__ == '__main__':
    main()