import asyncio
import board
import digitalio
import pwmio
from adafruit_motor import servo
from math import fabs

class ServoGo:
    def __init__(self, button_pin, servo_pin):
        self.button_pin = button_pin
        self.servo_pin = servo_pin
        # set up button/switch
        self.button = digitalio.DigitalInOut(button_pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        # servo
        self.servo_pwm = pwmio.PWMOut(servo_pin, duty_cycle=2**15, frequency=50)
        self.servo = servo.Servo(self.servo_pwm, min_pulse=300, max_pulse=2200)
        self.servo.angle = 90
        # stuff
        self.servo_target = 90

    def on_button(self,state):
        if not state:
            print("Pressed")
            self.servo_target = 180
        else:
            print("Not pressed")
            self.servo_target = 22

    async def watch_button(self, callback):
        last_state = self.button.value
        while True:
            state = self.button.value
            if state != last_state:
                callback(state)
                last_state = state
            await asyncio.sleep(0)

    async def servo_update(self):
        while True:
            a = self.servo.angle
            print(f"current angle: {a}")
            m = fabs(self.servo_target-a) 
            if m>2:
    #            if m>10: m=10
                dir = m if a<self.servo_target else -m
                n = a + dir #/5
                print(f"new angle: {n}")
                self.servo.angle = n
            await asyncio.sleep(0.1)


# pins
# button_pin = board.GP15
# servo_pin = board.GP0

hello1 = ServoGo(board.GP15, board.GP0)

async def main():
    await asyncio.gather(
        hello1.watch_button(hello1.on_button),
        hello1.servo_update(),
    )

asyncio.run(main())
