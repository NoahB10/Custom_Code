#Write scripts in this folder to run the syringe pump can vary the flow rates in time with multistepping 

# Import CHEMYX serial connection module/driver
from core import connect
import time 
print("Starting")
# MUST set baudrate in pump "System Settings", and MUST match this rate:
baudrate=9600
"""
ports = connect.getOpenPorts()  # Added function which checks if it is connected to the machine
#Select the port which is connected 
port = connect.COM_Test(ports)
print("Port is:", port)
if port is None:
    raise Exception("No pump found on any serial port.")
"""
# initiate Connection 
conn = connect.Connection(port='COM21',baudrate=baudrate, multipump=False)
#%% Connect and Run Pump - Basic Setup
if __name__=='__main__':
    # Open Connection to pump
    conn.openConnection()
    print("Connected")

    # Setup parameters for pump 
    direction = -1   #Make positive for infuse and negative for withdrae
    units='μL/min'		 	# OPTIONS: 'mL/min','mL/hr','μL/min','μL/hr'
    diameter=4.78          # 1ml syringe has diameter of 4.78

    """
    #For one pumping rate:
    volume = 200*direction              #A negative volume means Withdrawing
    rate = 50              
    runtime = direction*volume/rate   #Wont run if have a negative runtime 
    """

    #For running sequential pumping rates:
    volume=[100,200,200,200,150]   # Buffer then Standard then air  
    volume = [direction*volume[ii] for ii in range(len(volume))] # Update the direction for each pump. Can make direction an array if need to switch direction
    delay=[0.12,0.12,0.12,0.12]               # Delay in minutes
    rate=[50,40,100,40,100]         # rates for each of the sequential actions
    runtime= [direction*volume[ii]/rate[ii] for ii in range(len(rate))] # this is calculated implictly by pump

    """
    # Variable flow rates in each step, linear ramping generated by pump [REMEMBER TO SET multistep=True in startPump()]
    rate1=[20,5,40]         # between rate1 and rate2 for each step
    rate2=[50,6,41]         # use one rate list for linear flow per step
    varrates=[f'{rate1[ii]}/{rate2[ii]}' for ii in range(len(rate1))]
    # Rate = [Step1: 20mL/min->50mL/min, Step2: 5mL/min->6mL/min, Step3: 40mL/min->41mL/min]
    """

    # Communicate parameters to pump
    conn.setUnits(units)
    conn.setDiameter(diameter) 
    def send(volume,rate,delay): 
        #Need to have delays because otherwise the machine will not update the settings in time
        conn.setVolume(volume)   
        time.sleep(.3)    
        conn.setRate(rate) 
        time.sleep(.3)        
        conn.setDelay(delay) 
        time.sleep(.3) 
        conn.startPump()   # set multistep= True when varrying the rate of each step 
    
    # Simple function to return the integer time that has elapsed in minutes 
    def timeread():
        string = conn.getElapsedTime()
        string = string[1]
        numbers = string[15:22]# If the time of running will get past 10 minutes then change it to start at 14 
        numbers = float(numbers)
        return numbers
    
    for i in range(len(runtime)):
        send(volume[i],rate[i],delay[i])
        rounded_time = int(runtime[i]*1000 -1)/1000
        while timeread()<(rounded_time):
            time.sleep(0.05)
            print(timeread())
        time.sleep(.3)
    conn.closeConnection()

