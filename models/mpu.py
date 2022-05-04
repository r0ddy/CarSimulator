import smbus
import time
import math

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

class MPU:
    BUS = smbus.SMBus(1)

    def MPU_Init(self):
        #write to sample rate register
        self.BUS.write_byte_data(self.device_addr, SMPLRT_DIV, 7)
        
        #Write to power management register
        self.BUS.write_byte_data(self.device_addr, PWR_MGMT_1, 1)
        
        #Write to Configuration register
        self.BUS.write_byte_data(self.device_addr, CONFIG, 0)
        
        #Write to Gyro configuration register
        self.BUS.write_byte_data(self.device_addr, GYRO_CONFIG, 24)
        
        #Write to interrupt enable register
        self.BUS.write_byte_data(self.device_addr, INT_ENABLE, 1)

    def __init__(self, device_addr):
        self.device_addr = device_addr
        self.MPU_Init()

    def read_raw_data(self, addr):
	    #Accelero and Gyro value are 16-bit
        high = self.BUS.read_byte_data(self.device_addr, addr)
        low = self.BUS.read_byte_data(self.device_addr, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

    def read_gyro(self):
        gyro_x = self.read_raw_data(GYRO_XOUT_H)
        gyro_y = self.read_raw_data(GYRO_YOUT_H)
        gyro_z = self.read_raw_data(GYRO_ZOUT_H)
        return gyro_x, gyro_y, gyro_z

