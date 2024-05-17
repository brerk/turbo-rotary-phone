# https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_1-Wire_DS18B20_Sensor

import os
import glob
import time

# These two lines mount the device:
os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

base_dir = "/sys/bus/w1/devices/"

# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"


def read_rom():
    name_file = device_folder + "/name"
    f = open(name_file, "r")

    return f.readline()


def read_temp_raw():
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()

    return lines


def read_temp() -> float:
    lines = read_temp_raw()

    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()

    temp_string = lines[-1].split("t=")[1]  # Get value from string

    temp_c = float(temp_string) / 1000.0

    # TODO: reimplement using negative index
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find("t=")

    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos + 2 :]

        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0

        # return temp_c, temp_f
        return temp_c

    return None


if __name__ == "__main__":
    while True:
        temp_c = read_temp()

        if not temp_c:
            print("Couldn't read temperature from file.")
            continue

        # print(f"Temperature --> C: {temp_c:3.3f}, F: {temp_f:3.3f}")
        print(f"Temperature --> C: {temp_c:3.3f}")

        time.sleep(1)
