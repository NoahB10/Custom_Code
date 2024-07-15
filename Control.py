#Write scripts in this folder to run the syringe pump can vary the flow rates in time with multistepping 

# Import CHEMYX serial connection module/driver
from core import connect
print("Starting")
# MUST set baudrate in pump "System Settings", and MUST match this rate:
baudrate=9600
ports = connect.getOpenPorts()  # Added function which checks if it is connected to the machine
#Select the port which is connected 
port = connect.COM_Test(ports)
print("Port is:", port)
if port is None:
    raise Exception("No pump found on any serial port.")

# initiate Connection 
conn = connect.Connection(port='COM19',baudrate=baudrate, multipump=False)
#%% Connect and Run Pump - Basic Setup
if __name__=='__main__':
    # Open Connection to pump
    conn.openConnection()
    print("Connected")
    # Setup parameters for pump 1
    units='μL/min'		 	# OPTIONS: 'mL/min','mL/hr','μL/min','μL/hr'
    diameter=28.6           # 28.6mm diameter
    volume=200                # 1 mL volume
    rate=200                  # 1 mL/min flow rate
    runtime=volume/rate     # this is calculated implictly by pump
    delay=0.5               # 30 second delay
    
    # Communicate parameters to pump
    conn.setUnits(units)
    conn.setDiameter(diameter)  
    conn.setVolume(volume)      
    conn.setRate(rate)        
    conn.setDelay(delay)    
    
    # Start pump
    conn.startPump()