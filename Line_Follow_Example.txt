from hub import light_matrix
import runloop
import motor_pair
import color_sensor
import math
import time
from hub import port

async def main():
    # write your code here
    await light_matrix.write("Hi!")
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
    start_time = time.ticks_ms()
    while time.ticks_ms() - start_time < 5000: ##(follow the line for 5000 miliseconds or 5 seconds)
        motor_pair.move(motor_pair.PAIR_1, math.floor(-3/5*color_sensor.reflection(port.E)+30),velocity=280)
        ##steering uses gradient/intercept method equation y = mx + b
        #Y = steering value, x = light reflection, b = steering value when reflection is = 0
        #B =
        #when sensor = 50, steering = 0 (sees half way between white and black)
        #when sensor = 0, sterring = 30 (0 means sees black, steering right)
        #when sensor = 100, steering = -30 (100 means sees white, steering left)
        #steering = (m * reflected light) + 30  ##x is the unknown reflected light intensity value that is detected
        #M = -100/60 = -3/5 (negative 1 divided by the maximum and minimum of the steering range)
        #math.floor means no decimal
    motor_pair.stop(motor_pair.PAIR_1)

runloop.run(main())
