from servos import servos

# servos isna dictionary of initialised class wrapped pwms
# properties are numbers 1 to 5

def reinitialize(data):
    print("reinitializing...")
    print(data)
    for s in servos:
        smin = data[f"s{s}min"]
        smax = data[f"s{s}max"]
        sangle = data[f"s{s}"]
        servos[s].set_limits(smin, smax)
        servos[s].set_angle(sangle)

def realtime_update(msg):
    print("updating...")
    print(msg)
    key,value = msg.split(":")
    lk = list(key)
    s = lk[0]
    n = int(lk[1])
    rest = "".join(lk[2:])
    if len(rest)==0 and s=="s":
        print((n,value))
        servos[n].set_angle(int(value))
