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

# True extents of the servos for my setup
# 0       2
#   \ ^ /
#    888
#   /   \
# 1       3
# 
# 0 left front
# 1 left back
# 2 right front
# 3 right back
angle_pins = [0, 3, 6, 9]
top_pins = [1, 4, 7, 10]
bottom_pins = [2, 5, 8, 11]
spare_pins = [12, 13, 14, 15]

pin_dirs = [
     1,  1,  1, # FL
    -1, -1, -1, # BL
    -1, -1, -1, # FR
     1,  1,  1, # BR

    0, 0, 0, 0  # spares
]

legs = {
    0: [0, 1, 2], 
    1: [3, 4, 5],
    2: [6, 7, 8],
    3: [9, 10, 11]
}

extents = {
    angle_pins[0]: {
        "ext": [180, 520],  # forward -> backward
        "range": 520-180,
        "leg": 0,
        "type": "fwdback",
        },
    top_pins[0]: {
        "ext": [100, 360],  # out -> in
        "range": 360-100,
        "leg": 0,
        "type": "outin",
        },
    bottom_pins[0]: {
        "ext": [140, 500],  # up -> down
        "range": 500-140,
        "leg": 0,
        "type": "updown",
        },

    angle_pins[1]: {
        "ext": [140, 430],  # forward -> backward
        "range": 430-140,
        "leg": 1,
        "type": "fwdback",
        },
    top_pins[1]: {
        "ext": [120, 420],  # out -> in
        "range": 420-120,
        "leg": 1,
        "type": "outin",
        },
    bottom_pins[1]: {
        "ext": [140, 500],  # up -> down
        "range": 500-140,
        "leg": 1,
        "type": "updown",
        },

    angle_pins[2]: {
        "ext": [180, 520],  # forward -> backward
        "range": 520-180,
        "leg": 2,
        "type": "fwdback",
        },
    top_pins[2]: {
        "ext": [100, 360],  # out -> in
        "range": 360-100,
        "leg": 2,
        "type": "outin",
        },
    bottom_pins[2]: {
        "ext": [140, 500],  # up -> down
        "range": 500-140,
        "leg": 2,
        "type": "updown",
        },

    angle_pins[3]: {
        "ext": [140, 430],  # forward -> backward
        "range": 430-140,
        "leg": 3,
        "type": "fwdback",
        },
    top_pins[3]: {
        "ext": [120, 420],  # out -> in
        "range": 420-120,
        "leg": 3,
        "type": "outin",
        },
    bottom_pins[3]: {
        "ext": [140, 500],  # up -> down
        "range": 500-140,
        "leg": 3,
        "type": "updown",
        },
}


# pin_dirs = [1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 0, 0, 0, 0]

def move(pins, start, stop, step, smooth=5, p=False):
    '''Move servos from start to stop (absolute values)'''
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


def move_rel(pin, start_rel, stop_rel, step=1/40.0, smooth=5, p=False):
    '''Move one servo from start to stop (relative values)'''
    ext = extents[pin]['ext']
    rng = extents[pin]['range']
    start = round((start_rel * rng) + ext[0], 0)
    stop = round((stop_rel * rng) + ext[1], 0)
    if p:
        print(f"Moving pin {pin} ({extents[pin]['type']} Leg {extents[pin]['leg']}) from {start} to {stop}...")
    if stop<start:
        loop_dir = -1
    else:
        loop_dir = 1
    for pos in range(start, stop + 1, loop_dir * smooth):
        if p:
            print(pos, hi - pos + lo)
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
