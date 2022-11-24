import threading
import RPi.GPIO as GPIO
import time
import robotLight
from ultra import *

def ultrathread(u, delay):
    '''Update the ultrasonic sensor distance once per second
    '''
    try:
        while True:
            u.update_dist()
            time.sleep(delay)
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    u = ultraSensor()
    delay = 0.2

    RL = robotLight.RobotLight()
    RL.start()

    t = threading.Thread(target=ultrathread, args=(u, delay), daemon=True)

    try:
        t.start()
        for counter in range(0,201):
            if u.distance < 0.1 and RL.lightMode != 'police':
                logging.info("NO TOUCHY!!")
                RL.police()
            elif u.d <= 0.25 and RL.lightMode != 'police':
                logging.info("Too close!")
                RL.setColor(100,50,0)
            else:
                RL.pause()
            time.sleep(0.1)
    except:
        GPIO.cleanup()
        exit()
    finally:
        GPIO.cleanup()
        exit()

    GPIO.cleanup()
