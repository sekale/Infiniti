
import os, time, sys, signal, atexit

import pyupm_mma7660 as upmMMA7660

 


import pyupm_i2clcd as lcd

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS) 
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

#myLcd.setCursor(0,0)
# RGB Blue
#myLcd.setColor(53, 39, 249)

# RGB Red
#myLcd.setColor(255, 0, 0)

#myLcd.write('Hello World')
#myLcd.setCursor(1,2)
#myLcd.write('Hello World')

# Instantiate an MMA7660 on I2C bus 0

myDigitalAccelerometer = upmMMA7660.MMA7660(

                    upmMMA7660.MMA7660_I2C_BUS,

                    upmMMA7660.MMA7660_DEFAULT_I2C_ADDR);

## Exit handlers ##

# This function stops python from printing a stacktrace when you hit control-C

def SIGINTHandler(signum, frame):

    raise SystemExit

 

# This function lets you run code on exit, including functions from myDigitalAccelerometer

def exitHandler():

    print "Exiting"

    sys.exit(0)

# Register exit handlers


def output_command(x_val, y_val, z_val):


    if(y_val > 10):
        value = 0 #center
        if(os.path.exists("left")):
            os.remove("LEFT")
        if(os.path.exists("RIGHT")):
            os.remove("RIGHT")
        with open("CENTER", 'w') as input:
            print("here")
	myLcd.setColor(255,0,0)
	myLcd.write('Center')
    
        #print("here")

    elif(y_val >= -10 and y_val <= 10):
        value = 1 #right
        if(os.path.exists("RIGHT")):
            os.remove("RIGHT")
        if(os.path.exists("LEFT")):
            os.remove("LEFT")
        with open("CENTER", 'w') as input:
            print("here")
	myLcd.setColor(0,255,0)
        #print("here")

    elif(y_val < 10):
        value = -1 #left
        if(os.path.exists("CENTER")):
            os.remove("CENTER")
        if(os.path.exists("RIGHT")):
            os.remove("RIGHT")
        with open("LEFT", 'w') as input:
            print("here")
        #print("here")
	myLcd.setColor(0,0,255)

    else:
        value = 3 #exit the program
        #print("here")

    return value


atexit.register(exitHandler)

def main():

    signal.signal(signal.SIGINT, SIGINTHandler)


# place device in standby mode so we can write registers

    myDigitalAccelerometer.setModeStandby()

 

# enable 64 samples per second

    myDigitalAccelerometer.setSampleRate(upmMMA7660.MMA7660.AUTOSLEEP_64)

 

# place device into active mode

    myDigitalAccelerometer.setModeActive()

 

    x = upmMMA7660.new_intp()

    y = upmMMA7660.new_intp()

    z = upmMMA7660.new_intp()

 

    ax = upmMMA7660.new_floatp()

    ay = upmMMA7660.new_floatp()

    az = upmMMA7660.new_floatp()
    while (1):
        myDigitalAccelerometer.getRawValues(x, y, z)
        #print(x,y,z)
        outputStr = ("Raw values: x = {0}"
                     " y = {1}"
                     " z = {2}").format(upmMMA7660.intp_value(x),
                                        upmMMA7660.intp_value(y),

                                        upmMMA7660.intp_value(z))

        var1 = int(upmMMA7660.intp_value(x))
        var2 = int(upmMMA7660.intp_value(y))
        var3 = int(upmMMA7660.intp_value(z))

        print(output_command(var1, var2, var3))
 

#time.sleep(.5)

if __name__ == '__main__':
    main()
