#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import INA226_lib
import time
import os
import sys
import subprocess
import chardet
import csv
import datetime
import fcntl
import log_data_pb2
from google.protobuf import text_format

# INA226 I2C Slave address
INA226_ADDR_A0_GND_A1_GND = 0x40
INA226_ADDR_A0_VDD_A1_GND = 0x41
INA226_ADDR_A0_SDA_A1_GND = 0x42
INA226_ADDR_A0_SCL_A1_GND = 0x43
INA226_ADDR_A0_GND_A1_VDD = 0x44
INA226_ADDR_A0_VDD_A1_VDD = 0x45
INA226_ADDR_A0_SDA_A1_VDD = 0x46
INA226_ADDR_A0_SCL_A1_VDD = 0x47
INA226_ADDR_A0_GND_A1_SDA = 0x48
INA226_ADDR_A0_VDD_A1_SDA = 0x49
INA226_ADDR_A0_SDA_A1_SDA = 0x50
INA226_ADDR_A0_SCL_A1_SDA = 0x51
INA226_ADDR_A0_GND_A1_SCL = 0x52
INA226_ADDR_A0_VDD_A1_SCL = 0x53
INA226_ADDR_A0_SDA_A1_SCL = 0x54
INA226_ADDR_A0_SCL_A1_SCL = 0x55


# Settings
LOGGING_HZ = 100 # ログを取得する周期(Hz)
MINIMUM_LOG_LINES = LOGGING_HZ * 600  #最低限ログを保存しておく行数(10分相当分)
MAX_LOG_LINES = MINIMUM_LOG_LINES * 1.5 #この行数を超えたら、ログを上の行数まで減らす
I2CBUS = 1 # I2C通信に使用するBUS


# 関連するファイル

#ログを保存するファイル,シリアライズされたバイナリが保存されている
log_file_path = '/var/tmp/log_voltage_and_current.dat'
#現在のデータを参照したい時のためのファイル、最新のデータがテキストで保存されている
tmp_log_file_path = '/var/tmp/tmp_voltage_and_current.txt'
#ログを保存するファイル用のロックファイル
lock_log_file_path = '/var/tmp/lock_voltage_and_current.lock'


# ログファイルの行数を確認し、最大行数を超えていたら古いログを削除する. 削除した後の行数を返す
def truncateLogFile(current_lines):
    #ログの行数チェック
    if current_lines >= MAX_LOG_LINES:
        remove_num = current_lines - MINIMUM_LOG_LINES # MINIMUM_LOG_LINESまで行数を減らす
        
        log_file_fd = open(log_file_path, 'r+')
        lines = log_file_fd.readlines()
        log_file_fd.close()

        lines = lines[remove_num:]

        tmp_file = '/var/tmp/vc_tmp.dat'
        temp_log_file = open(tmp_file, 'w')
        temp_log_file.writelines(lines)
        temp_log_file.close()

        #余剰の行を削除して作った一時ファイルを新しいログファイルとして上書きする
        os.rename(tmp_file, log_file_path)
        return len(lines)
    else:
        return current_lines

#ロックを取得してログファイルに書き込む
def writeWithLock(data,loop_counter):
    #排他ロックの取得
    lock_file = open(lock_log_file_path, 'r+')
    fcntl.lockf(lock_file, fcntl.LOCK_EX)

    # ログファイルへの書き込み
    try:
        log_file = open(log_file_path, 'r+')
        log_file.write(data)
        log_file.close()
    finally:
        #排他ロックの解放
        fcntl.lockf(lock_file, fcntl.LOCK_UN)

def main():
    # ループカウンタ
    Loop_counter = 1 

    #INA226(i2c_Bus, i2c_slave_address, shunt_resistor_val)
    Switching_Power_Input = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_GND_A1_GND, 2)
    Battery_Input = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_VDD_A1_GND, 2)
    SBC_Power_Supply = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_SDA_A1_GND, 2)
    Actuator_Power_Supply = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_SCL_A1_GND, 2)
    # Device initialization
    Switching_Power_Input.Initialization()
    Battery_Input.Initialization()
    SBC_Power_Supply.Initialization()
    Actuator_Power_Supply.Initialization()

#ログファイルが存在するかの確認
    if os.path.isfile(log_file_path):
        pass
    else:
        with open(log_file_path, 'w') as log_file:
            log_file.write('\n')
            log_file.close()

    # ログファイルの行数確認と切り捨て
    current_log_lines_number = len(open(log_file_path).readlines())
    current_log_lines_number = truncateLogFile(current_log_lines_number)

#データの読み取りと保存のループ
    while(1):
        # protoを作成
        proto_data = log_data_pb2.PowerLog()

        # タイムスタンプをセット
        proto_data.timestamp.GetCurrentTime()
        # Switching_Power_Input を読み取って代入
        proto_data.Switching_Power_Input_mA = int(Switching_Power_Input.Read_mA())
        proto_data.Switching_Power_Input_mV = int(Switching_Power_Input.Read_mV())
        # Battery_Input_Power_Input を読み取って代入
        proto_data.Battery_Input_mA = int(Battery_Input.Read_mA())
        proto_data.Battery_Input_mV = int(Battery_Input.Read_mV())
        # SBC_Power_Supply を読み取って代入
        proto_data.SBC_Power_Supply_mA = int(SBC_Power_Supply.Read_mA())
        proto_data.SBC_Power_Supply_mV = int(SBC_Power_Supply.Read_mV())
        # Actuator_Power_Supply を読み取って代入        
        proto_data.Actuator_Power_Supply_mA = int(Actuator_Power_Supply.Read_mA())
        proto_data.Actuator_Power_Supply_mV = int(Actuator_Power_Supply.Read_mV())

        #データのシリアライズ
        serialized_data = proto_data.SerializeToString()

        #一時ファイルに書く用のテキストデータにも変換
        log_data_text = text_format.MessageToString(proto_data)

        # 一時ファイルに書きこみ
        with open(tmp_log_file_path, 'a') as file1:
            file1.write(log_data_text)
        file1.close()

        # ログファイルに書きこみ
        writeWithLock(serialized_data,Loop_counter)
        current_log_lines_number += 1

        #sleep
        time.sleep(1.0/LOGGING_HZ)

        Loop_counter += 1
        if Loop_counter % (LOGGING_HZ * 1200) == 0: #20分に一回行数チェックして切り捨てる
            current_log_lines_number = truncateLogFile(current_log_lines_number)

if __name__ == '__main__':
    main()
