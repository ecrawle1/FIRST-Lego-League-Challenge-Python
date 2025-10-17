from hub import port, motion_sensor
import motor, motor_pair, runloop, time

# Pair the drive motors on ports A and B
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

# Wheel + robot constants
WHEEL_DIAMETER_CM = 7.73
WHEEL_BASE_CM = 8.89# Distance between left/right wheels
CM_PER_INCH = 2.54
DEGREES_PER_ROTATION = 360

# Calculate wheel circumference
wheel_circumference_cm = WHEEL_DIAMETER_CM * 3.1416
degrees_per_cm = DEGREES_PER_ROTATION / wheel_circumference_cm
degrees_per_inch = degrees_per_cm * CM_PER_INCH

# PID constants for turning
Kp = 0.6
Ki = 0
Kd = 0

# DRIVE FUNCTION
async def drive_inches(inches, speed=180):
    degrees = int(inches * degrees_per_inch)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, 0, velocity=speed)

# PID TURN FUNCTION
async def pid_turn_to_yaw(target_yaw, velocity=60):
    motion_sensor.reset_yaw(0)
    integral = 0
    last_error = 0

    while True:
        current_yaw = motion_sensor.tilt_angles()[0]
        error = target_yaw - current_yaw

        if abs(error) < 1:
            break

        integral += error
        derivative = error - last_error
        last_error = error

        correction = Kp * error + Ki * integral + Kd * derivative
        correction = max(-100, min(100, int(correction)))

        print("Yaw:", current_yaw, "Error:", error, "Correction:", correction)

        motor_pair.move(motor_pair.PAIR_1, -correction, velocity=velocity)
        
        await runloop.sleep_ms(10)

    motor_pair.stop(motor_pair.PAIR_1)

# MAIN MISSION SEQUENCE
async def main():
    start_time = time.time()

    # Step 1: Drive forward 6.5 inches
    await drive_inches(6.5, speed=180)

    # Step 2: PID Turn right to 45 degrees
    await pid_turn_to_yaw(450, velocity=60)

    # Step 3: Drive forward 1.75 inches
    await drive_inches(4.75, speed=150)

    # Step 4: Run motor C left for 5 seconds at speed -50
    await motor.run_for_time(port.C, 5000, -50)

    # Step 5: Run motor D right for 5 seconds at speed 50
    await motor.run_for_time(port.D, 5000, 50)

    # Optional: Log time taken
    end_time = time.time()
    print("Mission completed in", round(end_time - start_time, 2), "seconds")

runloop.run(main())

