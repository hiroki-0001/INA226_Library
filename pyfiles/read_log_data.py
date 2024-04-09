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
    'timestamp_date',
    'timestamp_time',
    'system_boot_time_msec',
    'Switching_Power_Input_mA',
    'Switching_Power_Input_mV',
    'Battery_Input_mA',
    'Battery_Input_mV',
    'SBC_Power_Supply_mA',
    'SBC_Power_Supply_mV',
    'Actuator_Power_Supply_mA',
    'Actuator_Power_Supply_mV'
]

csv_header_20x = [ 
    'timestamp_date',
    'timestamp_time',
    'system_boot_time_msec',
    'Right_Switching_Power_Input_mA',
    'Right_Switching_Power_Input_mV',
    'Left_Switching_Power_Input_mA',
    'Left_Switching_Power_Input_mV',
    'Battery_Input',
    'Battery_Input_OK',
    'SBC_Power_Supply',
    'SBC_Power_Supply_OK'
]

def main():
    if len(sys.argv) > 1:
        output_file_path = sys.argv[1]
    else: 
        output_file_path = 'vol_and_cur_data.csv'
        print("If you want to change output file name, please input the name as an argument.")

    #排他ロックの取得
    print('read log data...\n This program may need some time. Please wait a moment.')
    try:
        lock_file = open(lock_log_file_path, 'r+')
    except FileNotFoundError:
        lock_file = open(lock_log_file_path, 'w+')
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
    # INAモジュールの種類によってヘッダーを変更
    env_var_value = os.getenv('INA_MODULE_TYPE')
    header_type = None
    if env_var_value == '20xTwin':
        header_type = csv_header_20x
    else:
        header_type = csv_header

    writer.writerow(header_type)
    line_count = 1
    start_time = 0
    prev_time = 0
    JST_time_zone = datetime.timezone(datetime.timedelta(hours=+9))
    for line in log_data_lines:
        log_data = None
        if env_var_value == '20xTwin':
            log_data = log_data_pb2.PowerLogTwinFor20x()
        else:
            log_data = log_data_pb2.PowerLog()

        try:
            log_data.ParseFromString(bytes.fromhex(line))
        except Exception as e:
            print("------- Error!!! -------")
            print(e)
            print("Error: line {0} is bad format ".format(line_count))
            exit(1)
        if abs(log_data.timestamp.ToMilliseconds() - prev_time) > 2000:
            start_time = log_data.timestamp.ToMilliseconds()
        prev_time = log_data.timestamp.ToMilliseconds()
        if env_var_value == '20xTwin':
            writer.writerow([
                log_data.timestamp.ToDatetime(JST_time_zone).strftime('%Y/%m/%d'),
                log_data.timestamp.ToDatetime(JST_time_zone).strftime('%H:%M:%S.%f'),
                log_data.timestamp.ToMilliseconds() - start_time,
                log_data.Right_Switching_Power_Input_mA,
                log_data.Right_Switching_Power_Input_mV,
                log_data.Left_Switching_Power_Input_mA,
                log_data.Left_Switching_Power_Input_mV,
                log_data.Battery_Input_mA,
                log_data.Battery_Input_mV,
                log_data.SBC_Power_Supply_mA,
                log_data.SBC_Power_Supply_mV,
            ])
        else:
            writer.writerow([
                log_data.timestamp.ToDatetime(JST_time_zone).strftime('%Y/%m/%d'),
                log_data.timestamp.ToDatetime(JST_time_zone).strftime('%H:%M:%S.%f'),
                log_data.timestamp.ToMilliseconds() - start_time,
                log_data.Switching_Power_Input_mA,
                log_data.Switching_Power_Input_mV,
                log_data.Battery_Input_mA,
                log_data.Battery_Input_mV,
                log_data.SBC_Power_Supply_mA,
                log_data.SBC_Power_Supply_mV,
                log_data.Actuator_Power_Supply_mA,
                log_data.Actuator_Power_Supply_mV
            ])
        line_count += 1
    output_file.close()
    print("write log data to {0}".format(output_file_path))


if __name__ == '__main__':
    main()
