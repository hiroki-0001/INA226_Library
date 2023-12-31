#!/usr/bin/python3

import sys
import subprocess
import datetime

argvs = sys.argv
if len(argvs) < 3:
    print("Usage: python get_ina_data_from_robot.py [target_robot(number)] [connect device(wifi or lan)]")
    sys.exit()

target_robot = argvs[1]
connect_device = argvs[2]
if connect_device != "wifi" and connect_device != "lan":
    print("connect_device Must be [lan or wifi]")
    sys.exit()

date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
output_file_name = "./" + target_robot + "_" + date +"_vol_and_cur_data.csv"

print("target_robot: " + target_robot)
print("output_file_name: " + output_file_name)
try:
    str_from_sshpass = subprocess.run(["sshpass"],check=True,capture_output=True)
except:
    print("Error: " + "command [sshpass] is not found. Please install.")
    sys.exit()

if connect_device == "wifi":
    try:
        subprocess.check_output(["sshpass -p cit" + target_robot + " ssh cit@192.168.4." + target_robot + " \"cd ~/INA226_Library/pyfiles; python3 read_log_data.py\""], shell=True)
        subprocess.check_output(["sshpass -p cit" + target_robot + " scp cit@192.168.4." + target_robot + ":~/INA226_Library/pyfiles/vol_and_cur_data.csv " + output_file_name],shell=True)
    except subprocess.CalledProcessError as e:
        print("Error: target ip 192.168.4.{} is not found. Trying 192.168.3.{} ...".format(target_robot,target_robot))
        subprocess.check_output(["sshpass -p cit" + target_robot + " ssh cit@192.168.3." + target_robot + " \"cd ~/INA226_Library/pyfiles; python3 read_log_data.py\""], shell=True)
        subprocess.check_output(["sshpass -p cit" + target_robot + " scp cit@192.168.3." + target_robot + ":~/INA226_Library/pyfiles/vol_and_cur_data.csv " + output_file_name],shell=True)
else:
    subprocess.run(["sshpass -p cit" + target_robot + " ssh cit@192.168.100." + target_robot + " \"cd ~/INA226_Library/pyfiles; python3 read_log_data.py\""], shell=True)
    subprocess.run(["sshpass -p cit" + target_robot + " scp cit@192.168.100." + target_robot + ":~/INA226_Library/pyfiles/vol_and_cur_data.csv " + output_file_name],shell=True)

print("[[ Successfully read log data from " + target_robot + " ]]")
print("[[ Saved as " + output_file_name + " ]]")
