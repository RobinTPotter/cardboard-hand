import machine
import time

class Servo:
    def __init__(self, pin_num, freq=50):
        self.pin = machine.Pin(pin_num, machine.Pin.OUT)
        self.pwm = machine.PWM(self.pin)
        self.pwm.freq(freq)

    def set_us(self, us):
        """Set pulse width in microseconds (usually 500–2500)."""
        self.pwm.duty_ns(us * 1000)  # MicroPython expects ns

    def release(self):
        self.pwm.deinit()
        self.pin.init(mode=machine.Pin.IN)

# Create 5 servo objects
servos = [
    Servo(17),  # pin 17
    Servo(16),  # pin 16
    Servo(4),   # pin 4
    Servo(5),   # pin 5
    Servo(18),  # pin 18
]

# Test sweep
while True:
    for s in servos:
        s.set_us(2400)   # max
    time.sleep(1.5)

    for s in servos:
        s.set_us(600)    # min
    time.sleep(1.5)
