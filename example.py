from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm=GPIO.PWM(11, 50)
pwm.start(0)

pwm.ChangeDutyCycle(5)
GPIO.output(11, True)
pwm.ChangeDutyCycle(2.3)
sleep(1)
GPIO.output(11, False)
pwm.ChangeDutyCycle(0)

pwm.stop()
GPIO.cleanup()