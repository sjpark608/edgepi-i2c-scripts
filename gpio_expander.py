from periphery import I2C

# Expander base address
# TODO: need to double check whether the rpi i2c takes 7bit addressing or 8bit addressing
EXP_TYPE_1 = 0x40
EXP_TYPE_2 = 0xE8
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

def get_dev_address_read(pannel):
    dev_addr_0 = 0
    dev_addr_1 = 0
    if pannel == 0:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_0[0]<<1) + READ
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_0[1]<<1) + READ
    if pannel == 1:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_1[0]<<1) + READ
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_1[1]<<1) + READ
    if pannel == 2:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_2[0]<<1) + READ
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_2[1]<<1) + READ
    if pannel == 3:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_3[0]<<1) + READ
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_3[1]<<1) + READ
    if pannel == 4:
        dev_addr_0 = EXP_TYPE_2 + (PANNEL_4[0]<<1) + READ
        dev_addr_1 = EXP_TYPE_2 + (PANNEL_4[1]<<1) + READ
    if pannel == 5:
        dev_addr_0 = EXP_TYPE_2 + (PANNEL_5[0]<<1) + READ
        dev_addr_1 = EXP_TYPE_2 + (PANNEL_5[1]<<1) + READ
    
    return [dev_addr_0, dev_addr_1]

def get_dev_address_write(pannel):
    dev_addr_0 = 0
    dev_addr_1 = 0
    if pannel == 0:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_0[0]<<1) + WRITE
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_0[1]<<1) + WRITE
    if pannel == 1:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_1[0]<<1) + WRITE
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_1[1]<<1) + WRITE
    if pannel == 2:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_2[0]<<1) + WRITE
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_2[1]<<1) + WRITE
    if pannel == 3:
        dev_addr_0 = EXP_TYPE_1 + (PANNEL_3[0]<<1) + WRITE
        dev_addr_1 = EXP_TYPE_1 + (PANNEL_3[1]<<1) + WRITE
    if pannel == 4:
        dev_addr_0 = EXP_TYPE_2 + (PANNEL_4[0]<<1) + WRITE
        dev_addr_1 = EXP_TYPE_2 + (PANNEL_4[1]<<1) + WRITE
    if pannel == 5:
        dev_addr_0 = EXP_TYPE_2 + (PANNEL_5[0]<<1) + WRITE
        dev_addr_1 = EXP_TYPE_2 + (PANNEL_5[1]<<1) + WRITE
    
    return [dev_addr_0, dev_addr_1]

# Read Oregs
def read_regs(i2c, dev_addxs, reg_addx):
    msgs = [I2C.Message(reg_addx, read = False), I2C.Message([0x00,0x00], read = True)]
    i2c.transfer(dev_addxs, msgs)
    return msgs[1].data

# Read Outputs
def read_output_regs(i2c, pannel):
    dev_addxs = get_dev_address_read(pannel)
    outputs = read_regs(i2c, dev_addxs, OUTPUT_0)
    print(outputs)
    return outputs

# Read Configs
def read_output_regs(i2c, pannel):
    dev_addxs = get_dev_address_read(pannel)
    configs = read_regs(i2c, dev_addxs, CONFIG_0)
    print(configs)
    return configs

# Write op



if __name__ == '__main__':
    # i2c_dev = I2C("/dev/i2c-10")
    cmd = None
    while cmd != 0:
        cmd = int(input("""
                menu
                ----
                 (0). exit
                 (1). Check Addresses
                """).strip())
        if cmd == 0:
            print('Exit program')
        elif cmd == 1:
            pannel = int(input("Input Pannel Number: ").strip())
            dev_addxs_r = get_dev_address_read(pannel)
            dev_addxs_w = get_dev_address_write(pannel)
            print(hex(dev_addxs_r[0]), hex(dev_addxs_r[1]))
            print(hex(dev_addxs_w[0]), hex(dev_addxs_w[1]))
        else:
            print(f'Invalid cmd = {cmd}')

    print('===================================================')