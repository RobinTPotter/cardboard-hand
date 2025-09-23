import machine
import time

def test(num = 17):
    pwm = machine.PWM(
        machine.Pin(num, machine.Pin.OUT)
    )
    k = 1000
    pwm.freq(50)
    pwm.duty_ns(2700*k)
    time.sleep(0.5)
    pwm.duty_ns(250*k)
    time.sleep(0.5)
    pwm.duty_ns(2700*k)
    time.sleep(0.5)
    pwm.duty_ns(250*k)
    time.sleep(0.5)
    pwm.deinit()

