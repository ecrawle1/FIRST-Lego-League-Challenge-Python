from hub import light_matrix
from hub import motion_sensor
from hub import port
from hub import sound
import runloop
import motor_pair
import distance_sensor
import force_sensor

async def main():
    # write your code here
    await light_matrix.write("Hi!")
    motion_sensor.set_yaw_face(motion_sensor.FRONT) ##Front is the default setting, but you can change this if applicable
    motion_sensor.reset_yaw(0) ##reset yaw angles
    motor_pair.pair(motor_pair.PAIR_1,port.A,port.B)

    # turn left 90 degress (python uses decidegrees)
    while motion_sensor.tilt_angles()[0] <900 :     ##getting yaw value from tuple (remember 0 = yaw, 1 = pitch, 2 = roll) 90 degrees is positive to the left of zero
        motor_pair.move(motor_pair.PAIR_1, -100)  ## negative 100 is the steering value of left
    motor_pair.stop(motor_pair.PAIR_1)

    # turn right 90 degrees (you have to reverse the symbols <, and +/-)
    while motion_sensor.tilt_angles()[0]>-900:  ## using yaw value, look for greater than - 90 (900) to turn right
        motor_pair.move(motor_pair.PAIR_1, 100) ## steering in a + direction is turning right
    motor_pair.stop(motor_pair.PAIR_1)

    #move forward until object within 10cm
    while True:
        if distance_sensor.distance(port.F) >100 or distance_sensor.distance(port.F)==-1:  ## if the distance sensor is more than 10cm or -1 (in error) 
            motor_pair.move(motor_pair.PAIR_1,0) # moving straight ahead, forward
        else:
            motor_pair.stop(motor_pair.PAIR_1) # stop robot
            break # break out of the loop
    motor_pair.stop(motor_pair.PAIR_1)

    #make a beep when force sensor is touched
    while True: 
        if force_sensor.pressed(port.A):
            sound.beep





runloop.run(main())
