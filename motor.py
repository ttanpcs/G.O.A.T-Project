from time import sleep
import RPi.GPIO as GPIO

class Motor: 
    def __init__(self, range, minduty, maxduty, pinnum, hertz):
        self.range = range
        self.minduty = minduty
        self.maxduty = maxduty
        self.pinnum = pinnum
        self.hertz = hertz

    def set_angle(self, angle):
        duty = (angle/self.range) * (self.maxduty - self.minduty) + self.minduty
        print(duty)

        GPIO.setup(self.pinnum, GPIO.OUT)
        pwm=GPIO.PWM(self.pinnum, self.hertz)
        pwm.start(0)

        GPIO.output(self.pinnum, True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.pinnum, False)
        pwm.ChangeDutyCycle(0)

        pwm.stop()
        GPIO.cleanup()