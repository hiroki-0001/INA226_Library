import matplotlib.pyplot as plt
import numpy as np

data_set = np.loadtxt(
    fname="ina.csv", #読み込むファイルのパスと名前
    dtype="float", #floatで読み込む
    delimiter=",", #csvなのでカンマで区切る
    skiprows=1, #1行目は読み込まない
    usecols=[i for i in range(2, 11)]
)

x = data_set[:, 0] #1列目をxに代入
y = data_set[:, 1:] #2列目以降をyに代入

plt.plot(x,y)

plt.title("INA226 data") #タイトル
plt.xlabel("Time") #x軸のラベル
plt.ylabel("variable data") #y軸のラベル
plt.legend(["Switching_Power_Input_mA","Switching_Power_Input_mV","Battery_Input_mA","Battery_Input_mV","SBC_Power_Supply_mA","SBC_Power_Supply_mV","Actuator_Power_Supply_mA","Actuator_Power_Supply_mV"]) 
plt.grid() #グリッド線を引く(引かなくてもいい別に)

plt.show() 