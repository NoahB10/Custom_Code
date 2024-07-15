from core import connect
import serial
import time
print("Starting")
# MUST set baudrate in pump "System Settings", and MUST match this rate:

ports = connect.getOpenPorts()  # Added function which checks if it is connected to the machine
port = connect.COM_Test(ports)
print(port)     


# initiate Connection object with first open port
# conn = connect.Connection(port=port,baudrate=baudrate, multipump=False)