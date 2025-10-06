from servos import servos

# servos isna dictionary of initialised class wrapped pwms
# properties are numbers 1 to 5

def reinitialize(data):
    print("reinitializing...")
    print(data)
    for s in servos:
        smin = int(data[f"s{s}min"])
        smax = int(data[f"s{s}max"])
        sangle = int(data[f"s{s}"])
        servos[s].set_limits(smin, smax)
        servos[s].set_angle(sangle)

def realtime_update(msg):
    #print("updating...")
    #print(msg)
    key,value = msg.split(":")
    lk = list(key)
    s = lk[0]
    n = int(lk[1])
    rest = "".join(lk[2:])
    if len(rest)==0 and s=="s":
        #print((n,value))
        servos[n].set_angle(int(value))
    elif rest=="max":
        servos[n].max = int(value)
    elif rest=="min":
        servos[n].min = int(value)

import random

def get_data():
    data = {}
    try:
        for s in servos:
            data[f"s{s}valmin"] = servos[s].min
            data[f"s{s}valmax"] = servos[s].max
            data[f"s{s}min"] = servos[s].min
            data[f"s{s}max"] = servos[s].max
            data[f"s{s}"] = servos[s].angle # + random.randrange(0,100)
            data[f"s{s}val"] = servos[s].angle  # + random.randrange(0,100)
            data[f"s{s}maxTxt"] = str(servos[s].max)
            data[f"s{s}minTxt"] = str(servos[s].min)
    except Exception as e:
        print(f"wha {e}")
    finally:
        return data
