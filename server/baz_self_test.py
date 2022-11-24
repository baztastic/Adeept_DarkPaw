import sys
from servo import *
from LED import *
from switch import *

try:
	if len(sys.argv) == 1:
		pinMin = 0
		pinMax = 12
	elif len(sys.argv) == 2:
		pinMin = 0
		pinMax = int(sys.argv[1])
	elif len(sys.argv) == 3:
		pinMin = int(sys.argv[1])
		pinMax = int(sys.argv[2])
		if pinMin == pinMax:
			pinMax = pinMax + 1
	else:
		print("Wrong number of arguments")
		exit(0)
except:
	print("Wrong type of argument(s)")
	exit(1)

try:
	switchSetup()
	led = LED()

	print("3 seconds til servo test...")

	led.colorWipe(100,100,100)
	switch(1,1)
	time.sleep(1)
	print("2...")

	led.colorWipe(50,50,50)
	time.sleep(1)
	print("1...")

	led.colorWipe(0,0,0)
	switch(1,0)
	time.sleep(1)
	print()
	print("Servo test:")

	while True:
		for pin in range(pinMin,pinMax):
			print("Pin:", pin)
			for i in range(0,10):
				pwm.set_pwm(pin, 0, (300+i*10))
				time.sleep(0.05)
			for i in range(0,20):
				pwm.set_pwm(pin, 0, (400-i*10))
				time.sleep(0.05)
			for i in range(0,10):
				pwm.set_pwm(pin, 0, (200+i*10))
				time.sleep(0.05)

except KeyboardInterrupt:
	print("\n\nReturn all to safe position.")
	for pin in range(pinMin,pinMax):
		pwm.set_pwm(pin, 0, 300)
	led.colorWipe(0,0,0)
	switch(1,0)
	exit(0)
