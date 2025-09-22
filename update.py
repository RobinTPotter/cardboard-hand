import machine

class Servo:
   def __init__(self, pin):
      self.pwm = machine.PWM(machine.Pin(pin, macine.Pin.OUT))
      self.update_cycle(1000,2000)
      self.angle(90)
   def update_cycle(self,min,max):
      self.min = min
      self.max = max
   def angle(self, angle):
      self.old_angle = self.angle
      self.angle = angle
      new_duty_ms = self.min + int(angle * float( self.max - self.min ) / 180.0)
      self.pwm.duty_us(new_duty_ms)

servos = [Servo(p) for p in [0,1,2,3,4]]

def reinitialize(data):
    print("reinitializing...")
    print(data)

def realtime_update(msg):
    print("updating...")
    print(msg)

