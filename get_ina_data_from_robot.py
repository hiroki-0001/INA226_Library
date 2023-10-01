#!/usr/bin/python3

import sys
import subprocess

argvs = sys.argv
if len(argvs) < 2:
    print("Usage: python get_ina_data_from_robot.py [target_robot(number)] optional:[output_file_name]")
    sys.exit()

target_robot = argvs[1]

if len(argvs) == 3:
    output_file_name = "./" + argvs[2]
else:
    output_file_name = "."

print("target_robot: " + target_robot)
print("output_file_name: " + output_file_name)
try:
    str_from_sshpass = subprocess.run(["sshpass"],check=True,capture_output=True)
except:
    print("Error: " + "command [sshpass] is not found. Please install.")
    sys.exit()

subprocess.run(["sshpass -p cit" + target_robot + " ssh cit@192.168.4." + target_robot + " \"cd ~/INA226_Library/pyfiles; python3 read_log_data.py\""], shell=True)
subprocess.run(["sshpass -p cit" + target_robot + " scp cit@192.168.4." + target_robot + ":~/INA226_Library/pyfiles/vol_and_cur_data.csv " + output_file_name],shell=True)

print("[[ Successfully read log data from " + target_robot + " ]]")
print("[[ Saved as " + output_file_name + " ]]")