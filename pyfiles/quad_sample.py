import INA226_lib
import time

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

#INA226(i2c_Bus, i2c_slave_address, shunt_resistor_val)
Switching_Power_Input = INA226_lib.INA226(8, INA226_ADDR_A0_GND_A1_GND, 2)
Battery_Input = INA226_lib.INA226(8, INA226_ADDR_A0_VDD_A1_GND, 2)
SBC_Power_Supply = INA226_lib.INA226(8, INA226_ADDR_A0_SDA_A1_GND, 2)
Actuator_Power_Supply = INA226_lib.INA226(8, INA226_ADDR_A0_SCL_A1_GND, 2)
# Device initialization
Switching_Power_Input.Initialization()
Battery_Input.Initialization()
SBC_Power_Supply.Initialization()
Actuator_Power_Supply.Initialization()



while(1):
    
    # read_data = []
    # Read Switching_Power_Input
    # Switching_Power_Input_mA = Switching_Power_Input.Read_mA()
    # Switching_Power_Input_mV = Switching_Power_Input.Read_mV()
    # # Read Battery_Input_Power_Input
    # Battery_Input_mA = Battery_Input.Read_mA()
    # Battery_Input_mV = Battery_Input.Read_mV()
    # # Read SBC_Power_Supply
    # SBC_Power_Supply_mA = SBC_Power_Supply.Read_mA()
    # SBC_Power_Supply_mV = SBC_Power_Supply.Read_mV()
    # Read Actuator_Power_Supply        
    Actuator_Power_Supply_mA = Actuator_Power_Supply.Read_mA()
    Actuator_Power_Supply_mV = Actuator_Power_Supply.Read_mV()
    # Add data to the list
    # read_data.append(Switching_Power_Input_mA)
    # read_data.append(Switching_Power_Input_mV)
    # read_data.append(Battery_Input_mA)
    # read_data.append(Battery_Input_mV)
    # read_data.append(SBC_Power_Supply_mA)
    # read_data.append(SBC_Power_Supply_mV)
    # read_data.append(Actuator_Power_Supply_mA)
    # read_data.append(Actuator_Power_Supply_mV)
    
    print("mA = {0}, mV = {1}".format(Actuator_Power_Supply_mA, Actuator_Power_Supply_mV))
    time.sleep(0.01)
