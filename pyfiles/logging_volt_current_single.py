#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import INA226_lib
import time
import os
import sys
import subprocess
import chardet

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

def main():
    
    I2CBUS = 1 # I2C通信に使用するBUS
    
    #INA226(i2c_Bus, i2c_slave_address, shunt_resistor_val)
    sample_device = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_GND_A1_GND, 2)
    sample_device.Initialization()
    tmp_file_fd = open("/var/tmp/voltage_and_current","w", encoding="utf_8", newline='\n')
    tmp_file_fd.close()
    os.chmod("/var/tmp/voltage_and_current", 0o777)
    os.chown("/var/tmp/voltage_and_current", 1000, 1000)
    
    if(os.path.isfile('/var/tmp/voltage_and_current_log')):
        os.chmod("/var/tmp/voltage_and_current_log", 0o777)
        os.chown("/var/tmp/voltage_and_current_log", 1000, 1000)
        
    else:
        log_file_fd = open("/var/tmp/voltage_and_current_log","w+", encoding="utf_8", newline='\n')
        log_file_fd.close()
        os.chmod("/var/tmp/voltage_and_current_log", 0o777)
        os.chown("/var/tmp/voltage_and_current_log", 1000, 1000)
    
    while(1):
        log_time = subprocess.check_output(['date', '+%Y年%m月%d日_%H時%M分%S秒'])
        timed_filename_str = log_time.decode(chardet.detect(log_time)["encoding"]).replace("\n", "")
        mA = sample_device.Read_mA()
        mV = sample_device.Read_mV()

        # write tmp file
        tmp_file_fd = open("/var/tmp/voltage_and_current","a", encoding="utf_8", newline='\n')
        tmp_file_fd.write("curent_mA:{}\n".format(mA))
        tmp_file_fd.write("voltage_mV:{}\n".format(mV))
        tmp_file_fd.close()
        
        # write log file
        log_file_fd = open("/var/tmp/voltage_and_current_log","r+", encoding="utf_8", newline='\n')
        lines = log_file_fd.readlines()
        if len(lines) >= 2000:
            lines = lines[1:]
            log_file_fd.seek(0)
            log_file_fd.truncate()
            log_file_fd.writelines(lines)
            
        log_file_fd.write("{}, curent_mA:{}, voltage_mV:{}\n".format(timed_filename_str, mA, mV))
        log_file_fd.close()
        
        time.sleep(0.5)

if __name__ == '__main__':
    main()
