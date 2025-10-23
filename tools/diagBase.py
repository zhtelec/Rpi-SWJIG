import      os
import      sys
from smbus2 import SMBus
import      time
#import      lgpio
import      select

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

val = 0
chip = 0


result = False
def ExecuteDiag(line):
    global result

    print("input string: [", end="")
    print(line, end="]\n")

    time.sleep(2)

    if result == True:
        result = False
    else:
        result = True

    return  result


# printOK
def PrintOK():
    print("  OOOO    KK    KK")
    print("OO    OO  KK  KK")
    print("OO    OO  KKKK")
    print("OO    OO  KKKK")
    print("OO    OO  KK  KK")
    print("  OOOO    KK    KK")

# printOK
def PrintNG():
    print("NN    NN    GGGG")
    print("NNN   NN  GG    GG")
    print("NNNN  NN  GG")
    print("NN NN NN  GG  GGGG")
    print("NN  NNNN  GG   GGG")
    print("NN   NNN    GGG GG")

# turn on
def TurnOnIo():
    val = SWJIG_EN_5V  | SWJIG_EN_3V | SWJIG_EN_GPIO | SWJIG_LED_ACT
    bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
    time.sleep(0.1)


# turn off
def TurnOffIo():
    val = 0
    bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)


# turn off and set OK LED
def TurnOffIo_OK():
    val = SWJIG_LED_OK
    bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)


# turn off and set NG LED
def TurnOffIo_NG():
    val = SWJIG_LED_NG
    bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)


def ClearConsole():
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)



with SMBus(1) as bus:  # I2c-1 bus of Raspberry Pi
    # port0-pin0 is input (sw)
    bus.write_byte_data(I2C_ADDRESS, PORT0_CONFIG, 0x01)
    bus.write_byte_data(I2C_ADDRESS, PORT1_CONFIG, 0x00)
    bus.write_byte_data(I2C_ADDRESS, PORT0_OUTPUT, 0)
    bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, 0)

#    chip = lgpio.gpiochip_open(4)

    val = 0
    bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)

    while True:
        print("# press sw to turn on")
        line = ""
        while (bus.read_byte_data(I2C_ADDRESS, PORT0_INPUT) & SWJIG_SW):
            if sys.stdin in select.select([sys.stdin], [], [], 0.01)[0]:
                line = sys.stdin.readline().strip()
                break;
        while (~bus.read_byte_data(I2C_ADDRESS, PORT0_INPUT) & SWJIG_SW):
            time.sleep(0.01)

        if(line == "exit"):
            exit(0)

        ClearConsole()
        print("# turn on [power and gpio]")
        sys.stdout.flush()
        TurnOnIo()

        print("# check target board")
        re = ExecuteDiag(line)
        print("")
        if(re == True):
             TurnOffIo_OK()
             PrintOK()
        else:
             TurnOffIo_NG()
             PrintNG()

        print("\n\n\n\n\n\n")
