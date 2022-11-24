import sys
from servo import *
from LED import *
from switch import *

speed = 40.0
step = 1/speed # seconds
smooth = 10

lo = 150
md = 300
hi = 450

angle_pins = [0, 3, 6, 9]
top_pins = [1, 4, 7, 10]
bottom_pins = [2, 5, 8, 11]
spare_pins = [12, 13, 14, 15]

pin_dirs = [1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 0, 0, 0, 0]

def move(pins, start, stop, step, smooth=5, p=False):
	if stop<start:
		loop_dir = -1
	else:
		loop_dir = 1
	for pos in range(start, stop + 1, loop_dir * smooth):
		if p:
			print(pos, hi - pos + lo)
		for pin in pins:
			if pin_dirs[pin] == -1:
				pin_pos = hi - pos + lo
			else:
				pin_pos = pos
			pwm.set_pwm(pin, 0, pin_pos)
		time.sleep(step)

def sit():
	move(bottom_pins + top_pins, md, lo, step, p=False)
	#move(top_pins, md, lo, step, p=False)

def stand():
	move(top_pins + bottom_pins, lo, md, step, p=False)
	#move(bottom_pins, lo, md, step, p=False)

if __name__ == "__main__":
	switchSetup()
	led = LED()

	led.colorWipe(0,0,0)  # turn off leds
	switch(1,0)  # turn off light
	sit()
	time.sleep(1)
	stand()
