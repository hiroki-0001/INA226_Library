#!/usr/bin/python3

import sys
import subprocess

argvs = sys.argv
if len(argvs) != 2:
    print("Usage: python get_ina_data_from_robot.py [target_robot(number)] ")
    sys.exit()

target_robot = argvs[1]


print("Target_robot: " + target_robot)

try:
    str_from_sshpass = subprocess.run(["sshpass"],check=True,capture_output=True)
except:
    print("Error: " + "command [sshpass] is not found. Please install.")
    sys.exit()

subprocess.run(["sshpass -p cit" + target_robot + " ssh cit@192.168.4." + target_robot + " \"cd ~/INA226_Library/pyfiles; python3 read_latest_data.py\""], shell=True)