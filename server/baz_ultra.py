'''
Output ultrasonic ranging results
'''
import RPi.GPIO as GPIO
import time
import logging
import threading
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")


def ultrasetup():
    Tr = 11 # Pin number of input terminal of ultrasonic module
    Ec = 8 # Pin number of output terminal of ultrasonic module

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Tr, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(Ec, GPIO.IN)
    logging.info(f"Setting up ultrasonic sensor on pins: {Tr} (Trigger) and {Ec} (Echo)")
    return(Tr, Ec)


def checkdist():
    if GPIO.getmode() != 11:
        Tr, Ec = ultrasetup()
    else:
        Tr = 11
        Ec = 8

    GPIO.output(Tr, GPIO.HIGH) # Set the input end of the module to high level and emit an initial sound wave
    time.sleep(0.000015)
    GPIO.output(Tr, GPIO.LOW)

    while not GPIO.input(Ec): # When the module no longer receives the initial sound wave
        pass
    t1 = time.time() # Note the time when the initial sound wave is emitted

    while GPIO.input(Ec): # When the module receives the return sound wave
        pass
    t2 = time.time() # Note the time when the return sound wave is captured

    dist = round((t2 - t1) * 340 / 2, 2) # Calculate distance (m)
    logging.info(f"Ultrasonic distance: {dist}")

    return dist


class ultraSensor:
    def __init__(self):
        self.trig, self.echo = ultrasetup()
        self.distance = 10
        self.dist_list = [self.distance] * 3
        self.d = sum(self.dist_list) / len(self.dist_list)
        self._lock = threading.Lock()

    def update_dist(self):
        logging.debug("Updating distance")
        with self._lock:
            local_distance = checkdist()
            local_dist_list = self.dist_list
            local_dist_list.pop()
            local_dist_list = [local_distance] + local_dist_list
            local_d = sum(local_dist_list) / len(local_dist_list)
            self.distance = local_distance
            self.dist_list = local_dist_list
            self.d = local_d
        logging.debug(f"Distance updated {self.dist_list}")


if __name__ == '__main__':
    try:
        while True:
                checkdist()
                time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
