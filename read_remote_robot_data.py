#!/usr/bin/python3

import sys
import subprocess

argvs = sys.argv
if len(argvs) != 3:
    print("Usage: python get_ina_data_from_robot.py [target_robot(number)] [connect devide(wifi or lan)] ")
    sys.exit()

target_robot = argvs[1]
connect_device = argvs[2]
if connect_device != "wifi" and connect_device != "lan":
    print("connect_device Must be [lan or wifi]")
    sys.exit()

print("Target_robot: " + target_robot)

try:
    str_from_sshpass = subprocess.run(["sshpass"],check=True,capture_output=True)
except:
    print("Error: " + "command [sshpass] is not found. Please install.")
    sys.exit()

if connect_device == "wifi":
    try :
        subprocess.check_output(["sshpass -p cit" + target_robot + " ssh cit@192.168.4." + target_robot + " \"cd ~/INA226_Library/pyfiles; python3 read_latest_data.py\""], shell=True)
    except:
        print("Error: replace address 4 to 3 and retry." )
        subprocess.run(["sshpass -p cit" + target_robot + " ssh cit@192.168.3." + target_robot + " \"cd ~/INA226_Library/pyfiles; python3 read_latest_data.py\""], shell=True)
else:
    subprocess.run(["sshpass -p cit" + target_robot + " ssh cit@192.168.100." + target_robot + " \"cd ~/INA226_Library/pyfiles; python3 read_latest_data.py\""], shell=True)