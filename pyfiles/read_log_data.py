#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fcntl
import log_data_pb2
import csv

# 関連するファイル

#ログを保存するファイル,シリアライズされたバイナリが保存されている
log_file_path = '/var/tmp/log_voltage_and_current.dat'
#ログを保存するファイル用のロックファイル
lock_log_file_path = '/var/tmp/lock_voltage_and_current.lock'

output_file_path = 'vol_and_cur_data.csv'

csv_header = [ 
    'timestamp',
    'Switching_Power_Input_mA',
    'Switching_Power_Input_mV',
    'Battery_Input_mA',
    'Battery_Input_mV',
    'SBC_Power_Supply_mA',
    'SBC_Power_Supply_mV',
    'Actuator_Power_Supply_mA',
    'Actuator_Power_Supply_mV'
]

def main():
    if len(sys.argv) > 1:
        output_file_path = sys.argv[1]
    else: 
        print("If you want to change output file name, please input the name as an argument.")

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
    
    output_file = open(output_file_path, 'w')
    writer = csv.writer(output_file, lineterminator='\n')
    writer.writerow(csv_header)
    for line in log_data_lines:
        log_data = log_data_pb2.LogData()
        log_data.ParseFromString(line)
        writer.writerow([
            proto_data.timestamp.ToDatetime().strftime('%Y/%m/%d %H:%M:%S.%f'),
            proto_data.Switching_Power_Input_mAs,
            proto_data.Switching_Power_Input_mVs,
            proto_data.Battery_Input_mAs,
            proto_data.Battery_Input_mVs,
            proto_data.SBC_Power_Supply_mAs,
            proto_data.SBC_Power_Supply_mVs,
            proto_data.Actuator_Power_Supply_mAs,
            proto_data.Actuator_Power_Supply_mV
        ])
    output_file.close()
    print("write log data to {0}".format(output_file_path))


if __name__ == '__main__':
    main()