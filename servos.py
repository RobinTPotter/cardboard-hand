import machine
import time

if "Pin" not in dir(machine):
    print("Using dummy machine")
    import dummymachine
    machine = dummymachine

class Pin:
    OUT = 0
    IN = 0
    def __init__(self,n, d):
        pass

class PWM:
    def __init__(self,a):
        pass
    def freq(self,f):
        pass
    def duty_ns(self,d):
        pass
    def deinit(self):
        pass

if "Pin" not in dir(machine):
    setattr(machine, "Pin", Pin)

if "PWM" not in dir(machine):
    setattr(machine, "PWM", PWM)

class Servo:
    def __init__(self, pin_num, freq=50):
        self.pin = machine.Pin(pin_num, machine.Pin.OUT)
        self.pwm = machine.PWM(self.pin)
        self.pwm.freq(freq)
        self.angle = 90
        self.min = 250
        self.max = 2230
        self.time_buffer = 100
        self.last_time = 0

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
        now = time.ticks_ms()
        angle = int(angle)
        if (self.last_time + self.time_buffer) < now:
            self.last_time = now
            self.angle = angle
            self.update()
        else:
            print("swallowed")

    def release(self):
        self.pwm.deinit()
        self.pin.init(mode=machine.Pin.IN)

# Create 5 servo objects
servos = {
    1:Servo(19),   # pin 19
    2:Servo(18),  # pin 18
    3:Servo(5),   # pin 5
    4:Servo(17),  # pin 17
    5:Servo(16),  # pin 16
}
