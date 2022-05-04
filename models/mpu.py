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
    def MPU_Init(self):
        #write to sample rate register
        self.bus.write_byte_data(self.device_addr, SMPLRT_DIV, 7)
        
        #Write to power management register
        self.bus.write_byte_data(self.device_addr, PWR_MGMT_1, 1)
        
        #Write to Configuration register
        self.bus.write_byte_data(self.device_addr, CONFIG, 0)
        
        #Write to Gyro configuration register
        self.bus.write_byte_data(self.device_addr, GYRO_CONFIG, 24)
        
        #Write to interrupt enable register
        self.bus.write_byte_data(self.device_addr, INT_ENABLE, 1)

    def __init__(self, device_addr, bus_num):
        self.device_addr = device_addr
        self.bus = smbus.SMBus(bus_num)
        self.MPU_Init()

    def read_raw_data(self, addr):
	    #Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.device_addr, addr)
        low = self.bus.read_byte_data(self.device_addr, addr+1)
    
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
    
    def read_accel(self):
        accel_x = self.read_raw_data(ACCEL_XOUT_H)
        accel_y = self.read_raw_data(ACCEL_YOUT_H)
        accel_z = self.read_raw_data(ACCEL_ZOUT_H)
        return accel_x, accel_y, accel_z

    def read_x_angle(self):
        x, y, z = self.read_accel()
        return get_x_rotation(x, y, z)

    def read_y_angle(self):
        x, y, z = self.read_accel()
        return get_y_rotation(x, y, z)

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

