#!/usr/bin/env python3
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import subprocess
from time import strftime
import time
import sys
import os


def readRegister(number):
    rr = client.read_input_registers(number, 1)
    value = rr.registers
    return float(value[0])


def getRegister(tmp_readregister, number1, number2=None):
    value = tmp_readregister.registers
    result = value[number1]
    if number2:
        result = result << 16
        result += value[number2]
    return float(result)


# READ VALUES FROM MODBUS SERIAL DEVICE (GROWATT INVERTER)
# choose the serial client
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)

try:
    client.connect()
    while 1 == 1:
        readregister = client.read_input_registers(0, 124)  # Read all registers in 1 go
        if not readregister.isError():
            for i in readregister:
                reg = getRegister(readregister, i)
                print("register", i, "has the value:", reg)

            time.sleep(5)
            os.system('clear')
            sys.stdout.flush()
except ModbusClient.exceptions.ConnectionException:
    print("No values to read from device, are you sure you are connected or the device is on?")