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
MAX_LOG_LINES = MINIMUM_LOG_LINES * 3 #この行数を超えたら、ログを上の行数まで減らす
SLEEP_TIME = 1.0 / LOGGING_HZ #ログを取るのに待つ間隔
I2CBUS = 1 # I2C通信に使用するBUS


# 関連するファイル

#ログを保存するファイル,シリアライズされたバイナリが保存されている
log_file_path = '/var/tmp/log_voltage_and_current.dat'
#現在のデータを参照したい時のためのファイル、最新のデータがテキストで保存されている
tmp_log_file_path = '/var/tmp/tmp_voltage_and_current.txt'
#ログを保存するファイル用のロックファイル
lock_log_file_path = '/var/tmp/lock_voltage_and_current.lock'

lock_file = None
log_file = None

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
def writeWithLock(data,loop_counter,lock_file_fd,log_file_fd):
    #排他ロックを一度解放する事で待ってる側に受け渡す
    if loop_counter % LOGGING_HZ == 0:    #一番最初とそれ以降は一秒毎に手放す
        #ファイルをクローズして排他ロックの解放 
        if not log_file_fd.closed:
            log_file_fd.close()
        if not lock_file_fd.closed:
            fcntl.lockf(lock_file_fd, fcntl.LOCK_UN)
            lock_file_fd.close()
        else:
            with open(lock_log_file_path, 'r+') as lockf:
                fcntl.lockf(lockf, fcntl.LOCK_UN)

        #排他ロックの取得
        lock_file_fd = open(lock_log_file_path, 'r+')
        fcntl.lockf(lock_file_fd, fcntl.LOCK_EX)
        log_file_fd = open(log_file_path, 'a')

    # ログファイルへの書き込み
    log_file_fd.write(data + '\n')

    return lock_file_fd,log_file_fd 

def main():

    global log_file
    global lock_file
    
    Switching_Power_Input = None
    Battery_Input =         None
    SBC_Power_Supply =      None
    Actuator_Power_Supply = None


    Switching_Power_Input_OK  = True
    Battery_Input_OK = True
    SBC_Power_Supply_OK = True
    Actuator_Power_Supply_OK = True

    bus_open_error = 0

    # ループカウンタ
    Loop_counter = 0

    #INA226(i2c_Bus, i2c_slave_address, shunt_resistor_val)

    # smbusのバス番号の候補
    bus_list = [1,7,8]
    for bus_id in bus_list:
        I2CBUS = bus_id
        try:
            Switching_Power_Input = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_GND_A1_GND, 2)
            Switching_Power_Input_OK = True
        except Exception as e:
            Switching_Power_Input_OK = False
            print(e)
        
        try:
            Battery_Input = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_VDD_A1_GND, 2)
            Battery_Input_OK = True
        except Exception as e:
            Battery_Input_OK = False
            print(e)
        
        try:
            SBC_Power_Supply = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_SDA_A1_GND, 2)
            SBC_Power_Supply_OK = True
        except Exception as e:
            SBC_Power_Supply_OK = False
            print(e)
        
        try:
            Actuator_Power_Supply = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_SCL_A1_GND, 2)
            Actuator_Power_Supply_OK = True
        except Exception as e:
            Actuator_Power_Supply_OK = False
            print(e)

        # Device initialization
        try:
            Switching_Power_Input.Initialization()
            Switching_Power_Input_OK = True
        except Exception as e:
            Switching_Power_Input_OK = False
            print(e)

        try:
            Battery_Input.Initialization()
            Battery_Input_OK = True
        except Exception as e:
            Battery_Input_OK = False
            print(e)

        try:
            SBC_Power_Supply.Initialization()
            SBC_Power_Supply_OK = True
        except Exception as e:
            SBC_Power_Supply_OK = False
            print(e)

        try:
            Actuator_Power_Supply.Initialization()
            Actuator_Power_Supply_OK = True
        except Exception as e:
            Actuator_Power_Supply_OK = False
            print(e)
        
        if (not Switching_Power_Input_OK) and (not Battery_Input_OK) and (not SBC_Power_Supply_OK) and (not Actuator_Power_Supply_OK):
            bus_open_error += 1
        else:
            print("i2cbus id is ",I2CBUS)
            break

    if bus_open_error == 2:
        print("Cannot open bus 1 and 8. Maybe i2c or INA226 has some problem")
        exit()

#ログファイルが存在するかの確認
    if os.path.isfile(log_file_path):
        pass
    else:
        with open(log_file_path, 'w') as tmpf:
            tmpf.write('\n')
            tmpf.close()

    # ログファイルの行数確認と切り捨て
    with open(log_file_path) as tmpf:
        current_log_lines_number = len(tmpf.readlines())
    current_log_lines_number = truncateLogFile(current_log_lines_number)

    #ログファイルとロックファイルのファイルディスクリプタのオープン
    lock_file = open(lock_log_file_path, 'r+')
    fcntl.lockf(lock_file, fcntl.LOCK_EX)
    log_file = open(log_file_path, 'a')

    #パフォーマンス計測用
    ave_time = 0

#データの読み取りと保存のループ
    while(1):
        start_time = time.perf_counter()
        # protoを作成
        proto_data = log_data_pb2.PowerLog()
        # タイムスタンプをセット
        proto_data.timestamp.GetCurrentTime()
        # Switching_Power_Input を読み取って代入
        if Switching_Power_Input_OK:
            proto_data.Switching_Power_Input_mA = int(Switching_Power_Input.Read_mA())
            proto_data.Switching_Power_Input_mV = int(Switching_Power_Input.Read_mV())
        # Battery_Input_Power_Input を読み取って代入
        if Battery_Input_OK:
            proto_data.Battery_Input_mA = int(Battery_Input.Read_mA())
            proto_data.Battery_Input_mV = int(Battery_Input.Read_mV())
        # SBC_Power_Supply を読み取って代入
        if SBC_Power_Supply_OK:
            proto_data.SBC_Power_Supply_mA = int(SBC_Power_Supply.Read_mA())
            proto_data.SBC_Power_Supply_mV = int(SBC_Power_Supply.Read_mV())
        # Actuator_Power_Supply を読み取って代入        
        if Actuator_Power_Supply_OK:
            proto_data.Actuator_Power_Supply_mA = int(Actuator_Power_Supply.Read_mA())
            proto_data.Actuator_Power_Supply_mV = int(Actuator_Power_Supply.Read_mV())

        #データのシリアライズ
        serialized_data = proto_data.SerializeToString()

        # ログファイルに書きこみ
        lock_file,log_file = writeWithLock(serialized_data.hex(),Loop_counter,lock_file,log_file)
        current_log_lines_number += 1

        elapsed_time = time.perf_counter() - start_time
        #sleep
        if(elapsed_time < SLEEP_TIME):
            time.sleep( SLEEP_TIME - elapsed_time)

        Loop_counter += 1
        if Loop_counter % (LOGGING_HZ * 1200) == 0: #20分に一回行数チェックして切り捨てる
            current_log_lines_number = truncateLogFile(current_log_lines_number)

        #パフォーマンス計測用
        # ave_time += elapsed_time
        # if Loop_counter % 100 == 0:
        #     print(ave_time / Loop_counter)

if __name__ == '__main__':
    main()
