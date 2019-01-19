
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime

led = 7
status = False
wait = 1
txt = ""
estado_actual1 = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

GPIO_TRIGGER = 12
GPIO_ECHO = 18

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
	StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

try:
        while True:
                time.sleep(wait)
		dist = distance()
                if (dist>20 and dist<50):
                        status = True
                        wait = 0.3
                        txt = ": Motion Detected so Lamp ON"
                elif (dist<20):
                        status = False
                        wait = 0.1
                        txt = ": Lamp OFF"
                GPIO.output(led, status)
                timex = strftime("%d-%m-%Y  %H:%M:%S", gmtime())
                print timex + txt + " dist: {:.{}f} cm".format( dist, 2)
        time.sleep(0.1) #
except (KeyboardInterrupt, SystemExit):
        pass
GPIO.cleanup()
print ("Program ended")
