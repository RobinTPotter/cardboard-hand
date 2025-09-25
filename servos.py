import machine
import time

class Servo:
    def __init__(self, pin_num, freq=50):
        self.pin = machine.Pin(pin_num, machine.Pin.OUT)
        self.pwm = machine.PWM(self.pin)
        self.pwm.freq(freq)
        self.angle = 90
        self.min = 500
        self.max = 2500

    def set_us(self, us):
        """Set pulse width in microseconds (usually 500–2500)."""
        print(f"setting pulse {us}")
        self.pwm.duty_ns(us * 1000)  # MicroPython expects ns

    def set_limits(self, min, max):
        self.min = int(min)
        self.max = int(max)
        print(f"limit set {min} {max}")
        self.update()

    def update(self):
        calc = self.min + float(self.angle) * (self.max - self.min ) / 180.0
        self.set_us(int(calc))

    def set_angle(self, angle):
        self.angle = angle
        self.update()

    def release(self):
        self.pwm.deinit()
        self.pin.init(mode=machine.Pin.IN)

# Create 5 servo objects
servos = {
    1:Servo(18),  # pin 18
    2:Servo(5),   # pin 5
    3:Servo(17),  # pin 17
    4:Servo(16),  # pin 16
    5:Servo(4),   # pin 4
}
