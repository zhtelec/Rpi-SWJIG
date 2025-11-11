#!/usr/bin/ptyhon3

import      os
import      sys
from smbus2 import SMBus
import      time
#import      lgpio
import      select
import      optparse

# i2c slave address of TCA9535
I2C_ADDRESS = 0x24

# register list of TCA9535
PORT0_INPUT        = 0x00
PORT1_INPUT        = 0x01
PORT0_OUTPUT       = 0x02
PORT1_OUTPUT       = 0x03
PORT0_POLARITY     = 0x04
PORT1_POLARITY     = 0x05
PORT0_CONFIG       = 0x06  # 1 = input, 0 = output
PORT1_CONFIG       = 0x07

SWJIG_EN_5V        = 0x01
SWJIG_EN_3V        = 0x02
SWJIG_EN_GPIO      = 0x04
SWJIG_LED_OK       = 0x20
SWJIG_LED_NG       = 0x40
SWJIG_LED_ACT      = 0x80
SWJIG_SW           = 0x01

RESULT_OK          = True
RESULT_NG          = False

i2cBus  = 1
i2cAddr = I2C_ADDRESS
turnon  = False


# turn on
def TurnOnIo(bus, i2cAddr):
    val = SWJIG_EN_5V  | SWJIG_EN_3V | SWJIG_EN_GPIO | SWJIG_LED_ACT
    bus.write_byte_data(0x26, PORT1_OUTPUT, val)


# turn off
def TurnOffIo(bus, i2cAddr):
    val = 0
    bus.write_byte_data(i2cAddr, PORT1_OUTPUT, val)


def ParseOptions():
    global i2cBus
    global i2cAddr
    global turnon

    parser = optparse.OptionParser()
    #parser.add_option('-o', '--output',  dest='output',  help='output file')
    parser.add_option('',   '--i2cbus',  dest='i2cBus',                   help=f"set i2c address default {I2C_BUS}")
    parser.add_option('',   '--i2caddr', dest='i2cAddr', type="string",   help=f"set i2c address default 7\'h{I2C_ADDRESS:x}")
    parser.add_option('',   '--on',      dest='on',  action="store_true", help="force turn on")
    parser.add_option('',   '--off',     dest='off', action="store_true", help="force turn off")
    options, args = parser.parse_args()

    i2cBus  = int(options.i2cBus)      if options.i2cBus  is not None else I2C_BUS
    i2cAddr = int(options.i2cAddr, 16) if options.i2cAddr is not None else I2C_ADDRESS
    turnon  = True  if options.on  is not None else turnon
    turnon  = False if options.off is not None else turnon


def main():
    ParseOptions()

    with SMBus(i2cBus) as bus:  # I2c-1 bus of Raspberry Pi
        try:
            bus.write_byte_data(i2cAddr, PORT1_CONFIG, 0x00)
            if(turnon == True):
                TurnOnIo(bus, i2cAddr)
            else:
                TurnOffIo(bus, i2cAddr)

        except:
            print(f"gpio extender address is used 7\'h{i2cAddr:x}")
            print("please check i2c address, execute \"i2cdetect -y 1\"")


main()
