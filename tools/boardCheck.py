import      os
import      sys
from smbus2 import SMBus
import      time
import      lgpio

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

val = 0
chip = 0

listGpio = [4, 17, 27, 22, 10,9, 11, 0, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21 ]


def TurnOnIo():
        global   val

        # ACT LED on
        print("ACT, ", end="")
        sys.stdout.flush()
        val |= SWJIG_LED_ACT
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # 5V on
        print("5v, ", end="")
        sys.stdout.flush()
        val |= SWJIG_EN_5V
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # 3.3V on
        print("3.3v, ", end="")
        sys.stdout.flush()
        val |= SWJIG_EN_3V
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # GPIO en
        print("3.3v, ", end="")
        sys.stdout.flush()
        val |= SWJIG_EN_GPIO
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # NG LED on
        print("NG, ", end="")
        sys.stdout.flush()
        val |= SWJIG_LED_NG
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # OK LED on
        print("OK]")
        sys.stdout.flush()
        val |= SWJIG_LED_OK
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)



def TurnOffIo():
        global   val

        # OK LED off
        print("OK, ", end="")
        sys.stdout.flush()
        val &= ~SWJIG_LED_OK
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # NG LED off
        print("NG, ", end="")
        sys.stdout.flush()
        val &= ~SWJIG_LED_NG
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # GPIO dis
        print("GPIO, ", end="")
        sys.stdout.flush()
        val &= ~SWJIG_EN_GPIO
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # 3V dis
        print("3.3V, ", end="")
        sys.stdout.flush()
        val &= ~SWJIG_EN_3V
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # 5V dis
        print("5V, ", end="")
        sys.stdout.flush()
        val &= ~SWJIG_EN_5V
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)

        # ACT off
        print("ACT]")
        sys.stdout.flush()
        val &= ~SWJIG_LED_ACT
        bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)
        time.sleep(0.5)


def ToggleGpio(bus):
    global  chip
    port = 0

    j = 0
    while j < len(listGpio):
        port = listGpio[j]

        print (port, end=", ")
        sys.stdout.flush()
        i = 0
        while (bus.read_byte_data(I2C_ADDRESS, PORT0_INPUT) & SWJIG_SW):
            i += 1
            if i == 5:
                try:
                    lgpio.gpio_write(chip, port, 1)
                except Exception:
                    pass
            if i == 10:
                try:
                    lgpio.gpio_write(chip, port, 0)
                except Exception:
                    pass
                i = 0
            time.sleep(0.01)
        try:
            lgpio.gpio_write(chip, port, 0)
        except Exception:
            pass
        while (~bus.read_byte_data(I2C_ADDRESS, PORT0_INPUT) & SWJIG_SW):
            time.sleep(0.01)
        j += 1

def ClearConsole():
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)



with SMBus(1) as bus:  # I2c-1 bus of Raspberry Pi
    # port0-pin0 is input (sw)
    bus.write_byte_data(I2C_ADDRESS, PORT0_CONFIG, 0x01)
    bus.write_byte_data(I2C_ADDRESS, PORT1_CONFIG, 0x00)
    bus.write_byte_data(I2C_ADDRESS, PORT0_OUTPUT, 0)
    bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, 0)

    chip = lgpio.gpiochip_open(4)
 
    val = 0
    bus.write_byte_data(I2C_ADDRESS, PORT1_OUTPUT, val)

    while True:
        print("# press sw to turn on")
        while (bus.read_byte_data(I2C_ADDRESS, PORT0_INPUT) & SWJIG_SW):
            time.sleep(0.01)
        while (~bus.read_byte_data(I2C_ADDRESS, PORT0_INPUT) & SWJIG_SW):
            time.sleep(0.01)

        ClearConsole()
        print("# turn on [", end="")
        sys.stdout.flush()
        TurnOnIo()

        print("# check gpio")
        ToggleGpio(bus)
        print("")
  
        print("# press sw to turn off")
        while  (bus.read_byte_data(I2C_ADDRESS, PORT0_INPUT) & SWJIG_SW):
            time.sleep(0.01)
        while (~bus.read_byte_data(I2C_ADDRESS, PORT0_INPUT) & SWJIG_SW):
            time.sleep(0.01)

        print("# turn off [", end="")
        sys.stdout.flush()
        TurnOffIo()

