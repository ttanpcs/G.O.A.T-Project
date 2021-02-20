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
        self.angle = init_angle

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

        GPIO.setup(self.pinnum, GPIO.OUT)
        pwm=GPIO.PWM(self.pinnum, self.hertz)
        pwm.start(0)

        GPIO.output(self.pinnum, True)
        pwm.ChangeDutyCycle(duty)
        sleep(.5)
        GPIO.output(self.pinnum, False)
        pwm.ChangeDutyCycle(0)

        pwm.stop()
        GPIO.cleanup()
        self.angle = angle
