#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import datetime
import fcntl
import log_data_pb2
import paho.mqtt.client as mqtt

#ログを保存するファイル,シリアライズされたバイナリが保存されている
log_file_path = '/var/tmp/log_voltage_and_current.dat'
#ログを保存するファイル用のロックファイル
lock_log_file_path = '/var/tmp/lock_voltage_and_current.lock'

class INAStreamer:
    def __init__(self):
        # MQTT Brokerの接続情報
        self.broker_address = "192.168.75.220"
        self.broker_port = 1883
        self.client = mqtt.Client()
        self.client.connect(self.broker_address, self.broker_port)
        self.log_topic = "INA226_data"
        pass

    def stream_data(self):
        #排他ロックの取得
        lock_file = open(lock_log_file_path, 'r+')
        fcntl.lockf(lock_file, fcntl.LOCK_EX)

        # ログファイルの読み込み
        read_succeed = True
        try:
            log_file = open(log_file_path, 'r')
            last_line = log_file.readlines()[-1]
            log_file.close()
        except Exception as e:
            print(e)
            read_succeed = False
        finally:
            #排他ロックの解放
            fcntl.lockf(lock_file, fcntl.LOCK_UN)
        if not read_succeed:
            return
        
        log_data = None
        env_var_value = os.getenv('INA_MODULE_TYPE')
        if env_var_value == '20xTwin':
            log_data = log_data_pb2.PowerLogTwinFor20x()
        else:
            log_data = log_data_pb2.PowerLog()
        log_data.ParseFromString(bytes.fromhex(last_line))
        JST_time_zone = datetime.timezone(datetime.timedelta(hours=+9))
        time_str = "date time :: {}".format(log_data.timestamp.ToDatetime(JST_time_zone).strftime('%Y/%m/%d %H:%M:%S.%f'))
        print(time_str)
        print(log_data)
        # テキストとしてlog_dataを送信
        self.client.publish(self.log_topic, time_str + "\n" + str(log_data))

if __name__ == '__main__':
    print("streaming data...")
    streamer = INAStreamer()
    while True:
        streamer.stream_data()
        time.sleep(5) #5秒に一回送る