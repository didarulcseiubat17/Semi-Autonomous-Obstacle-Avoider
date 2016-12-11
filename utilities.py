# defines and setups the GPIO pins
from GPIO_pinouts import *

# necessary parameters defined here
from parameters import *


# FUNCTIONS

def mpuRead(imu):
    while not imu.IMURead():
        pass

    data = imu.getIMUData()
    fusionPose = data["fusionPose"]
    Gyro = data["gyro"]
    Accel = data["accel"]

    # values in radian
    yaw = fusionPose[2]
    yawrate = Gyro[2]

    acc_x = Accel[0] * 981
    acc_y = Accel[1] * 981

    ############################
    # print("ROLL = " + str(roll))
    # print("PITCH = " + str(pitch))
    # print("YAW = " + str(yaw))
    # print("ROLL_RATE = " + str(rollrate))
    # print("PITCH_RATE = " + str(pitchrate))
    # print("YAW_RATE = " + str(yawrate))
    # print("Accelation X: " + str(acc_x))
    # print("Accelation Y: " + str(acc_y))
    # print("Accelation Z: " + str(acc_z))
    # print(data)
    ############################

    return acc_x, acc_y, yaw, yawrate


def leftMotorForward(dc=100):
    leftp.ChangeDutyCycle(dc)
    GPIO.output(leftStepPinForward, GPIO.HIGH)
    GPIO.output(leftStepPinBackward, GPIO.LOW)


def leftMotorStop():
    GPIO.output(leftStepPinForward, GPIO.LOW)
    GPIO.output(leftStepPinBackward, GPIO.LOW)


def leftMotorBackward(dc=100):
    leftp.ChangeDutyCycle(dc)
    GPIO.output(leftStepPinForward, GPIO.LOW)
    GPIO.output(leftStepPinBackward, GPIO.HIGH)


def rightMotorForward(dc=100):
    rightp.ChangeDutyCycle(dc)
    GPIO.output(rightStepPinForward, GPIO.HIGH)
    GPIO.output(rightStepPinBackward, GPIO.LOW)


def rightMotorStop():
    GPIO.output(rightStepPinForward, GPIO.LOW)
    GPIO.output(rightStepPinBackward, GPIO.LOW)


def rightMotorBackward(dc=100):
    rightp.ChangeDutyCycle(dc)
    GPIO.output(rightStepPinForward, GPIO.LOW)
    GPIO.output(rightStepPinBackward, GPIO.HIGH)


def forward():
    leftMotorForward(left_motor_dc)
    rightMotorForward(right_motor_dc)


def backward():
    leftMotorBackward(left_motor_dc)
    rightMotorBackward(right_motor_dc)


def turnLeft():
    leftMotorStop()
    rightMotorForward(right_motor_dc)


def turnRight():
    rightMotorStop()
    leftMotorForward(left_motor_dc)


def forwardAdjust(yaw, yawrate):
    diff = yawRateFactor * yawrate
    if yawrate > yawRateThreshold:
        right_motor_dc = 100
        left_motor_dc = 100 - diff

    elif yawrate < -yawRateThreshold:
        left_motor_dc = 100
        right_motor_dc = 100 - diff

    print("R_DC = " + str(right_motor_dc) + " L_DC = " + str(left_motor_dc))
