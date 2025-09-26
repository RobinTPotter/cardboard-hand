# cardboard-hand

wireless access point for an esp32/pico

serves a page with sliders for the 5 servos used for fingers

![construction pic](./images/sketch.jpg)

very rough sketch, figers were one piece each from 4 ply cereal box card (pva laminate)

each joint was scored

![construction pic](./images/hand.jpg)

each joint used paper straw (superglue) and hair bands used for digit extesion. each joint has a tiny securing node at the top reverse to secure the band.

_17-9-25_

![construction pic](./images/holder.jpg)
![construction pic](./images/inplace.jpg)

housing for servos. will likely need securing better. should get the other 2 on the other side. not sure yet where or how to mount the "wrist".

added some code from chatgpt and https://docs.micropython.org/en/latest/esp32/quickref.html

_26-9-25_

![construction pic](./images/hand-circuit.jpg)

esp32s arrived, code complete or thereabouts. hotspot and page http://192.168.4.1/

had to install mpremote. commands are:

```
mpremote fs cp *html *py :
mpremote connect /dev/ttyUSB0
```

repl appears `ctrl+d` to run `main.py`

reset button is quicker
