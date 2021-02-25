from time import sleep
import RPi.GPIO as GPIO

class Motor: 
    def __init__(self, range, minduty, maxduty, pinnum, hertz, flipped, init_angle):
        self.range = range
        self.minduty = minduty
        self.maxduty = maxduty
        self.pinnum = pinnum
        self.hertz = hertz
        self.flipped = flipped
        if (flipped):
            self.angle = 180 - init_angle
        else:
            self.angle = angle

    def set_angle_with_stall(self, angle, stall_motor):
        if self.flipped:
            angle = 180 - angle
        while (self.angle > angle):
            if (self.angle - angle > 5):
                self.rotate_to_angle_increment_with_stall(self.angle - 5, stall_motor)
            else:
                self.rotate_to_angle_increment_with_stall(angle, stall_motor)
        while (self.angle < angle):
            if (angle - self.angle > 5):
                self.rotate_to_angle_increment_with_stall(self.angle + 5, stall_motor)
            else:
                self.rotate_to_angle_increment_with_stall(angle, stall_motor)
        
    def set_angle(self, angle):
        if self.flipped:
            angle = 180 - angle
        while (self.angle > angle):
            if (self.angle - angle > 5):
                self.rotate_to_angle_increment(self.angle - 5)
            else:
                self.rotate_to_angle_increment(angle)
        while (self.angle < angle):
            if (angle - self.angle > 5):
                self.rotate_to_angle_increment(self.angle + 5)
            else:
                self.rotate_to_angle_increment(angle)
        

    def stall(self, stalltime):
        sleep(stalltime)

    def rotate_to_angle_increment(self, angle):
        duty = (angle/self.range) * (self.maxduty - self.minduty) + self.minduty
        print(duty)

        GPIO.setup(self.pinnum, GPIO.OUT)
        pwm=GPIO.PWM(self.pinnum, self.hertz)
        pwm.start(0)

        GPIO.output(self.pinnum, True)
        pwm.ChangeDutyCycle(duty)
        sleep(.25)
        GPIO.output(self.pinnum, False)
        pwm.ChangeDutyCycle(0)

        pwm.stop()
        if (self.flipped):
            self.angle = 180 - angle
        else:
            self.angle = angle

    def rotate_to_angle_increment_with_stall(self, angle, stall_motor):
        
        duty = (angle/self.range) * (self.maxduty - self.minduty) + self.minduty
        stall_duty = (stall_motor.angle/stall_motor.range) * (stall_motor.maxduty - stall_motor.minduty) + stall_motor.minduty

        print("" + str(duty) + " " + str(stall_duty))
        GPIO.setup(self.pinnum, GPIO.OUT)
        GPIO.setup(stall_motor.pinnum, GPIO.OUT)
        pwm=GPIO.PWM(self.pinnum, self.hertz)
        pwm_stall = GPIO.PWM(stall_motor.pinnum, stall_motor.hertz)
        pwm.start(0)
        pwm_stall.start(0)

        GPIO.output(self.pinnum, True)
        pwm.ChangeDutyCycle(duty)
        pwm_stall.ChangeDutyCycle(stall_duty)
        sleep(.25)
        GPIO.output(self.pinnum, False)
        pwm.ChangeDutyCycle(0)
        pwm_stall.ChangeDutyCycle(0)

        pwm.stop()
        if (self.flipped):
            self.angle = 180 - angle
        else:
            self.angle = angle
