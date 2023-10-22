from smbus2 import SMBus
import yaml
import time

class INA226_offset_bias:
    
    def __init__(self):
        with open('/etc/INA226_offset.yaml', 'r') as yml:
            self.config = yaml.safe_load(yml)
            print (self.config)
    
    def modify_Sensor_Value(self, mA, address):
        if address == 0x40:
            return (mA + (self.config['address40']['param'] * (mA / 1000)))
        elif address == 0x41:
            return (mA + (self.config['address41']['param'] * (mA / 1000)))
        elif address == 0x42:
            return (mA + (self.config['address42']['param'] * (mA / 1000)))
        elif address == 0x43:
            return (mA + (self.config['address43']['param'] * (mA / 1000)))
        else:
            return "This sensor address is not supported"

class INA226:
    #INA226 Constant & Register address
    INA226_LSB_BUS = 1.25
    INA226_CONFIG_REG = 0x00
    INA226_BUSV_REG = 0x02
    INA226_POWER_REG = 0x03
    INA226_CURRENT_REG = 0x04
    INA226_CALIBRATION_REG = 0x05
    INA226_Manufacturer_ID_REG = 0xFE
    
    def __init__(self, i2c_Bus, i2c_slave_address, shunt_resistor_val):
        self.i2c = SMBus(i2c_Bus)
        self.slave_address = i2c_slave_address
        self.shunt_resistor_val = shunt_resistor_val
        self.offset = INA226_offset_bias()

    def Calibration_Data_Set(self):
        return 5120 / self.shunt_resistor_val
    
    def Register_Write(self, register_addr, data):
        data_array = []
        data_array.append(int(data) >> 8)
        data_array.append(int(data) & 0xff)
        self.i2c.write_i2c_block_data(self.slave_address, register_addr, data_array)
    
    def Register_Read(self, register_addr):
        read_data = []
        read_data = self.i2c.read_i2c_block_data(self.slave_address, register_addr, 2)
        data = read_data[0] << 8 | read_data[1]
        return data
        
    def Initialization(self):
        self.Register_Write(self.INA226_CONFIG_REG, 0xC127)
        whoiam = self.Register_Read(self.INA226_Manufacturer_ID_REG)

        if(whoiam == 21577):
            print("Slave address = {0} : INA226 device connect successful".format(hex(self.slave_address)))
        else:
            print("connect error!")
        
        calibration_data = self.Calibration_Data_Set()
        self.Register_Write(self.INA226_CALIBRATION_REG, calibration_data)
        time.sleep(1)

    def Read_mV(self):
        busVoltage = self.Register_Read(self.INA226_BUSV_REG)
        mV = busVoltage * self.INA226_LSB_BUS
        return mV

    def Read_mA(self):
        mA = self.Register_Read(self.INA226_CURRENT_REG)
        if mA >= 32768:
            mA =  mA - 65536
        
        return self.offset.modify_Sensor_Value(mA, self.slave_address)
    

