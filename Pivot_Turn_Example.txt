from hub import port
import runloop
import motor, motor_pair
import math

# Constants
WHEEL_DIAMETER_INCHES = 7.73
WHEEL_CIRCUMFERENCE = math.pi * WHEEL_DIAMETER_INCHES

# Initialize paired motors on A and B
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
drive_pair = motor_pair.PAIR_1

# Conversion helper
def inches_to_degrees(inches):
    return round((inches / WHEEL_CIRCUMFERENCE) * 360)
    # truncating value to int always rounds down.. ie 2.999 = 2, use round instead to get more accuracy

# Drive a number of inches
def move_inches(inches, speed=500):
    degrees = inches_to_degrees(inches)
    motor_pair.move_for_degrees(drive_pair, abs(degrees), 0, velocity=speed)

# Turn in place (pivot-style)
#def turn_in_place(turn_degrees, speed=500):
    #turn_ratio = 5.5# Adjust this based on robot geometry
    #turn_inches = (turn_degrees / 360) * (math.pi * turn_ratio)
    #degrees = inches_to_degrees(turn_inches)
    #motor_pair.move_for_degrees(drive_pair, int(degrees), 100, velocity=speed)

def turn_in_place(turn_degrees, speed=500):
    TRACK_WIDTH = 3.4375# inches, center to center of drive wheels
    turn_arc = (turn_degrees / 360) * (math.pi * TRACK_WIDTH)
    motor_degrees = round(inches_to_degrees(turn_arc))
    motor_pair.move_for_degrees(drive_pair, motor_degrees, 100, velocity=speed)

# Activate motor C
def activate_motor_C(degrees):
    motor.run_for_degrees(port.C, degrees, 100)
    #run_for_degrees from motor does not like 'velocity=' or 'speed=' but will allow a typed int

# Example program
async def main():
    move_inches(12)            # Drive forward 12 inches
    turn_in_place(90)          # Turn 90 degrees
    move_inches(-6)            # Drive backward 6 inches
    activate_motor_C(360)      # Rotate Motor C one full turn

runloop.run(main())


