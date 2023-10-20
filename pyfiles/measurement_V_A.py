import INA226_lib
import csv

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

I2CBUS = 1
SAMPLE_DATA_NUM = 5
data_header = ['data1', 'data2', 'data3', 'data4', 'data5', 'mean', 'median']

def calc_mean(list_data):
    return sum(list_data) / len(list_data)

def calc_median(list_data):
    half = SAMPLE_DATA_NUM // 2
    list_data.sort()
    return list_data[half]

def main():
    #INA226(i2c_Bus, i2c_slave_address, shunt_resistor_val)
    sample_device = INA226_lib.INA226(I2CBUS, INA226_ADDR_A0_SDA_A1_GND, 2)
    sample_device.Initialization()
    
    with open("measure_data3.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data_header)
    
    print("mode select V(Volt) or A(An)")
    measure_type = input()
    print("{0} measure mode ".format(measure_type))
    print("measure count ?")    
    measure_count = int(input())
    print("count = {0}",format(measure_count))    
    
    for i in range(measure_count):
        list_all_data = []
        list_measure_data = []
        print("currrent loop No.{0}".format(i+1))
        print("")
        check_input = input()
            
        for j in range(SAMPLE_DATA_NUM):
            if(measure_type == 'V' ):
                data = sample_device.Read_mV()
            else:
                data = sample_device.Read_mA()
                
            list_measure_data.append(data)
            list_all_data.append(data)
        try:
            list_all_data.append(calc_mean(list_measure_data))
            list_all_data.append(calc_median(list_measure_data))
        except ZeroDivisionError:
            print("ゼロ除算が発生しました")
                    
        with open("measure_data3.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(list_all_data)
        
if __name__ == "__main__":
    main()