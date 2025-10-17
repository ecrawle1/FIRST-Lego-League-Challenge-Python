from hub import port, motion_sensor
import motor_pair, runloop, color_sensor
import math

# Pair motors A & B
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

# Constants
WHEEL_DIAMETER_CM = 6.24 # SPIKE Prime standard wheel
THRESHOLD = 50    # Replace with value from Mission 1

# Calculate degrees per inch based on wheel diameter
def degrees_per_inch(diameter_cm):
    circumference_in_inches = (math.pi * diameter_cm) / 2.54
    return 360 / circumference_in_inches

DEGREES_PER_INCH = degrees_per_inch(WHEEL_DIAMETER_CM)

# Check if sensor sees black
def sees_black():
    return color_sensor.reflection(port.E) < THRESHOLD

async def main():
    # ✅ Step 1: Drive forward 9 inches
    degrees = int(12 * DEGREES_PER_INCH)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, 0, velocity=600)
    await runloop.sleep_ms(500)

    # ✅ Step 2: Turn left 90°
    motion_sensor.reset_yaw(0)
    motor_pair.move(motor_pair.PAIR_1, -100, velocity=200)
    while motion_sensor.tilt_angles()[0] < 800:# 90.0 degrees in tenths
        await runloop.sleep_ms(10)
    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(500)

    # ✅ Step 3: Drive forward until black line is detected
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=600)
    while not sees_black():
        await runloop.sleep_ms(10)
    motor_pair.stop(motor_pair.PAIR_1)

runloop.run(main())
