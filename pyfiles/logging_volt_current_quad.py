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
    #INA226(i2c_Bus, i2c_slave_address, shunt_resistor_val)
    Switched_mode_power = INA226_lib.INA226(8, INA226_ADDR_A0_GND_A1_GND, 2)
    Battery_power = INA226_lib.INA226(8, INA226_ADDR_A0_VDD_A1_GND, 2)
    SBC_power = INA226_lib.INA226(8, INA226_ADDR_A0_SDA_A1_GND, 2)
    Motor_power = INA226_lib.INA226(8, INA226_ADDR_A0_SCL_A1_GND, 2)
    Switched_mode_power.Initialization()
    Battery_power.Initialization()
    SBC_power.Initialization()
    Motor_power.Initialization()
    
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
        # read current
        Switched_mode_power_mA = Switched_mode_power.Read_mA()
        Battery_power_mA = Battery_power.Read_mA()
        SBC_power_mA = SBC_power.Read_mA()
        Motor_power_mA = Motor_power.Read_mA()
        # read volt
        Switched_mode_power_mV = Switched_mode_power.Read_mV()
        Battery_power_mV = Battery_power.Read_mV()
        SBC_power_mV = SBC_power.Read_mV()
        Motor_power_mV = Motor_power.Read_mV()

        # write tmp file
        tmp_file_fd = open("/var/tmp/voltage_and_current","a", encoding="utf_8", newline='\n')
        tmp_file_fd.write(
            "Switched_mode_power_mA:{},\
            Battery_power_mA:{},\
            SBC_power_mA:{},\
            Motor_power_mA:{},"
            .format(
                Switched_mode_power_mA, 
                Battery_power_mA, 
                SBC_power_mA, 
                Motor_power_mA
                )
            )
        tmp_file_fd.write(
            "Switched_mode_power_mV:{},\
            Battery_power_mV:{},\
            SBC_power_mV:{},\
            Motor_power_mV:{}, \n"
            .format(
                Switched_mode_power_mV,
                Battery_power_mV,
                SBC_power_mV,
                Motor_power_mV
                )
            )

        tmp_file_fd.close()
        
        # write log file
        log_file_fd = open("/var/tmp/voltage_and_current_log","r+", encoding="utf_8", newline='\n')
        lines = log_file_fd.readlines()
        if len(lines) >= 1200:
            lines = lines[1:]
            log_file_fd.seek(0)
            log_file_fd.truncate()
            log_file_fd.writelines(lines)
            
        log_file_fd.write(
            "{},\
            Switched_mode_power_mA:{},\
            Switched_mode_power_mV:{},\
            Battery_power_mA:{},\
            Battery_power_mV:{},\
            SBC_power_mA:{},\
            SBC_power_mV:{},\
            Motor_power_mA:{}\
			Motor_power_mV:{}\
			\n"
            .format(
                timed_filename_str,
                Switched_mode_power_mA, 
                Switched_mode_power_mV,
                Battery_power_mA, 
                Battery_power_mV,
                SBC_power_mA, 
                SBC_power_mV,
                Motor_power_mA,
                Motor_power_mV
                )
            )
        
        log_file_fd.close()
        time.sleep(0.5)

if __name__ == '__main__':
    main()
