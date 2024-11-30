from pymodbus import pymodbus_apply_logging_config
from pymodbus.client import ModbusSerialClient

from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse

from periphery import I2C
import time
import logging
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Expander base address
# TODO: need to double check whether the rpi i2c takes 7bit addressing or 8bit addressing
EXP_TYPE_1 = 0x20 #010 0[A2,A1,A0]
EXP_TYPE_2 = 0x74 #111 01[A1,A0]
# Front Pannel
PANNEL_0 = [0, 1]
PANNEL_1 = [2, 3]
PANNEL_2 = [4, 5]
PANNEL_3 = [6, 7]
PANNEL_4 = [0, 1]
PANNEL_5 = [2, 3]
# Read/Write Bit
READ = 0
WRITE = 1
# Register Addresses
OUTPUT_0 = 2
OUTPUT_1 = 3
CONFIG_0 = 6
CONFIG_1 = 7
# Channels
A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6
H = 7
I = 8
J = 9
#RBG
RED = 0
BLUE = 1
GREEN = 2
# Ch_RBG_pins
A_RGB = [0,1,2]
B_RGB = [3,4,5]
C_RGB = [6,7,8]
D_RGB = [9,10,11]
E_RGB = [12,13,14]
F_RGB = [15,0,1]
G_RGB = [2,3,4]
H_RGB = [5,6,7]
I_RGB = [8,9,10]
J_RGB = [11,12,13]
# Expander Pin addressing
EXP_PINS = [A_RGB,B_RGB,C_RGB,D_RGB,E_RGB,F_RGB,G_RGB,H_RGB,I_RGB,J_RGB]


def get_dev_address(pannel):
    dev_addr_0 = 0
    dev_addr_1 = 0
    if pannel == 0:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_0[0])
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_0[1])
    if pannel == 1:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_1[0])
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_1[1])
    if pannel == 2:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_2[0])
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_2[1])
    if pannel == 3:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_3[0])
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_3[1])
    if pannel == 4:
        dev_addr_0 = EXP_TYPE_2 + (PANNEL_4[0])
        dev_addr_1 = EXP_TYPE_2 + (PANNEL_4[1])
    if pannel == 5:
        dev_addr_0 = EXP_TYPE_2 + (PANNEL_5[0])
        dev_addr_1 = EXP_TYPE_2 + (PANNEL_5[1])
    
    return [dev_addr_0, dev_addr_1]

# Read Oregs
def read_regs(i2c, dev_addxs, reg_addx):
    msgs = [I2C.Message([reg_addx], read = False), I2C.Message([0x00,0x00], read = True)]
    i2c.transfer(dev_addxs, msgs)
    return msgs[1].data

# Read Outputs
def read_output_regs(i2c, pannel):
    dev_addxs = get_dev_address(pannel)
    print(dev_addxs)
    outputs = read_regs(i2c, dev_addxs[0], OUTPUT_0)
    print(outputs)
    outputs = read_regs(i2c, dev_addxs[1], OUTPUT_0)
    print(outputs)    
    return outputs

# Read Configs
def read_config_regs(i2c, pannel):
    dev_addxs = get_dev_address(pannel)
    configs = read_regs(i2c, dev_addxs[0], CONFIG_0)
    print(configs)
    configs = read_regs(i2c, dev_addxs[1], CONFIG_0)
    print(configs)
    return configs

# Write op
def write_regs(i2c, dev_addxs, reg_addx, data):
    msgs = [I2C.Message([reg_addx]+data, read = False)]
    i2c.transfer(dev_addxs, msgs)

# Write Outputs
def write_output_regs(i2c, pannel, pin):
    dev_addxs = get_dev_address(pannel)
    pins = 65535
    if pin<16:
        pins = [(pins&~(1<<pin))&0xFF, (pins&~(1<<pin))>>8]
        write_regs(i2c, dev_addxs[0], OUTPUT_0, pins)
    elif pin>=16:
        pin = pin-16
        pins = [(pins&~(1<<pin))&0xFF, (pins&~(1<<pin))>>8]
        write_regs(i2c, dev_addxs[1], OUTPUT_0, pins)
    # write_regs(i2c, dev_addxs[0], OUTPUT_0, pins)
    # write_regs(i2c, dev_addxs[1], OUTPUT_0, [255,255])

# Write Configs
def write_config_regs(i2c, pannel, data):
    dev_addxs = get_dev_address(pannel)
    print(dev_addxs)
    write_regs(i2c, dev_addxs[0], CONFIG_0, data)
    write_regs(i2c, dev_addxs[1], CONFIG_0, data)

def turn_off_led(i2c, pannel, ch, color):
    outputs = read_output_regs(i2c,pannel)
    print(outputs)
    # Combine two 8 bits into 16bit for toggling pin
    output_16 = outputs[1]<<8 + outputs[0]
    output_16 = output_16 & ~(1<<EXP_PINS[ch][color])
    # Break the combined number into 8bits to write back to the register
    outputs[1] = output_16>>8
    outputs[0] = output_16&0xFF
    write_output_regs(i2c, pannel, outputs)

def turn_on_led(i2c, pannel, ch, color):
    outputs = read_output_regs(i2c,pannel)
    print(outputs)
    # Combine two 8 bits into 16bit for toggling pin
    output_16 = outputs[1]<<8 + outputs[0]
    output_16 = output_16 | ~(1<<EXP_PINS[ch][color])
    # Break the combined number into 8bits to write back to the register
    outputs[1] = output_16>>8
    outputs[0] = output_16&0xFF
    write_output_regs(i2c, pannel, outputs)

def project_christmas_light(i2c_dev, pannel, pins):
    read_output_regs(i2c_dev,pannel)
    write_output_regs(i2c_dev,pannel, pins)
    read_output_regs(i2c_dev,pannel)
    read_config_regs(i2c_dev,pannel)
    write_config_regs(i2c_dev,pannel, [0,0])
    read_config_regs(i2c_dev,pannel)

def serial_test(client, num_dev, start):
    client.connect()
    for nth in range(num_dev):
        regs = client.read_holding_registers(1,10,start+nth)
        _logger.info(f"Serial Num: {(regs.registers[0]<<16) + regs.registers[1]},  FW Ver: {regs.registers[4]>>8}.{regs.registers[4]&0xFF}, Dev ID: {regs.registers[9]}, nth: {nth}")
    client.close()

if __name__ == '__main__':
    i2c_dev = I2C("/dev/i2c-10")
    client = ModbusSerialClient( "/dev/ttyUSB0", retries=3, baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=1)


    cmd = None
    while cmd != 0:
        cmd = int(input("""
                menu
                ----
                 (0). exit
                 (1). Check Addresses
                 (2). Read GPIO
                """).strip())
        if cmd == 0:
            print('Exit program')
        elif cmd == 1:
            pannel = int(input("Input Pannel Number: ").strip())
            dev_addxs_r = get_dev_address(pannel)
            dev_addxs_w = get_dev_address(pannel)
            print(hex(dev_addxs_r[0]), hex(dev_addxs_r[1]))
            print(hex(dev_addxs_w[0]), hex(dev_addxs_w[1]))
        elif cmd == 2:
            for i in range(30):

                read_output_regs(i2c_dev,4)
                write_output_regs(i2c_dev,4, i)
                read_output_regs(i2c_dev,4)
                read_config_regs(i2c_dev,4)
                write_config_regs(i2c_dev,4, [0,0])
                read_config_regs(i2c_dev,4)

                read_output_regs(i2c_dev,1)
                write_output_regs(i2c_dev,1, i)
                read_output_regs(i2c_dev,1)
                read_config_regs(i2c_dev,1)
                write_config_regs(i2c_dev,1, [0,0])
                read_config_regs(i2c_dev,1)

                read_output_regs(i2c_dev,2)
                write_output_regs(i2c_dev,2, i)
                read_output_regs(i2c_dev,2)
                read_config_regs(i2c_dev,2)
                write_config_regs(i2c_dev, 2, [0,0])
                read_config_regs(i2c_dev,2)

                read_output_regs(i2c_dev,3)
                write_output_regs(i2c_dev,3, i)
                read_output_regs(i2c_dev,3)
                read_config_regs(i2c_dev,3)
                write_config_regs(i2c_dev,3, [0,0])
                read_config_regs(i2c_dev,3)

                read_output_regs(i2c_dev,5)
                write_output_regs(i2c_dev,5, i)
                read_output_regs(i2c_dev,5)
                read_config_regs(i2c_dev,5)
                write_config_regs(i2c_dev,5, [0,0])
                read_config_regs(i2c_dev,5)

                time.sleep(1)
        if cmd == 3:
            serial_test(client, 25,200)
            serial_test(client, 25,101)
        else:
            print(f'Invalid cmd = {cmd}')

    print('===================================================')