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

MAX_LOG_LINES = 2000  #ログを保存する最大の行数
I2CBUS = 1 # I2C通信に使用するBUS


def main():
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

    header = [
        'Timestamp', 
        'Switching_Power_Input_mA',
        'Switching_Power_Input_mV',
        'Battery_Input_mA',
        'Battery_Input_mV',
        'SBC_Power_Supply_mA',
        'SBC_Power_Supply_mV',
        'Actuator_Power_Supply_mA',
        'Actuator_Power_Supply_mV'
    ]

    with open('/var/tmp/voltage_and_current.csv', 'w') as file1:
        writer = csv.writer(file1)
        writer.writerow(header)

    if os.path.isfile('/var/tmp/voltage_and_current_log.csv'):
        pass

    else:
        with open('/var/tmp/voltage_and_current_log.csv', 'w') as file2:
            writer = csv.writer(file2)
            writer.writerow(header)

    while(1):
        # log_time = subprocess.check_output(['date', '+%Y年%m月%d日_%H時%M分%S秒'])
        # timed_filename_str = log_time.decode(chardet.detect(log_time)["encoding"]).replace("\n", "")
        log_time = datetime.datetime.now()
        timed_filename_str = log_time.strftime("%Y-%m-%d-%H:%M:%S")
        read_data = []
        # Read Switching_Power_Input
        Switching_Power_Input_mA = Switching_Power_Input.Read_mA()
        Switching_Power_Input_mV = Switching_Power_Input.Read_mV()
        # Read Battery_Input_Power_Input
        Battery_Input_mA = Battery_Input.Read_mA()
        Battery_Input_mV = Battery_Input.Read_mV()
        # Read SBC_Power_Supply
        SBC_Power_Supply_mA = SBC_Power_Supply.Read_mA()
        SBC_Power_Supply_mV = SBC_Power_Supply.Read_mV()
        # Read Actuator_Power_Supply        
        Actuator_Power_Supply_mA = Actuator_Power_Supply.Read_mA()
        Actuator_Power_Supply_mV = Actuator_Power_Supply.Read_mV()
        # Add data to the list
        read_data.append(timed_filename_str)
        read_data.append(Switching_Power_Input_mA)
        read_data.append(Switching_Power_Input_mV)
        read_data.append(Battery_Input_mA)
        read_data.append(Battery_Input_mV)
        read_data.append(SBC_Power_Supply_mA)
        read_data.append(SBC_Power_Supply_mV)
        read_data.append(Actuator_Power_Supply_mA)
        read_data.append(Actuator_Power_Supply_mV)



        # write tmp file
        with open('/var/tmp/voltage_and_current.csv', 'a') as file1:
            writer = csv.writer(file1)
            writer.writerow(read_data)
        file1.close()

        #排他ロックの取得
        lock_file = open('current_voltage_log_lock.lock', 'w+')
        fcntl.lockf(lock_file, fcntl.LOCK_EX)

        # write log file
        log_file = open('/var/tmp/voltage_and_current_log.csv', 'r+')
        lines = log_file.readlines()

        if len(lines) >= MAX_LOG_LINES:
            log_file.close()
            remove_num = len(lines) - MAX_LOG_LINES
            lines = lines[remove_num:]
            temp_log_file = open('/var/tmp/vc_tmp.csv', 'w')
            temp_log_file.writelines(lines)
            writer = csv.writer(temp_log_file)
            writer.writerow(read_data)
            temp_log_file.close()
            os.rename('/var/tmp/vc_tmp.csv', '/var/tmp/voltage_and_current_log.csv')
        else:
            writer = csv.writer(log_file)
            writer.writerow(read_data)
            log_file.close()
        
        #排他ロックの解放
        fcntl.lockf(lock_file, fcntl.LOCK_UN)

        #sleep
        time.sleep(0.5)

if __name__ == '__main__':
    main()
