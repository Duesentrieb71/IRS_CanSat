import time
from lib.ibus import IBus

ibus_in = IBus(1, 115200, 10)


while True:
    res = ibus_in.read()
    # if signal then display immediately
    if (res[0] == 1):
        print ("Status {} CH 1 {} Ch 2 {} Ch 3 {} Ch 4 {} Ch 5 {} Ch 6 {} Ch 7 {} Ch 8 {} Ch 9 {} Ch 10 {}".format(
            res[0],    # Status
            IBus.normalize(res[1]),
            IBus.normalize(res[2]),
            IBus.normalize(res[3]),
            IBus.normalize(res[4]),
            IBus.normalize(res[5], type="dial"),
            IBus.normalize(res[6], type="dial"),
            IBus.normalize(res[7]),
            IBus.normalize(res[8]),
            IBus.normalize(res[9]),
            IBus.normalize(res[10])),
            end="")
        print (" - {}".format(time.ticks_ms()))
    else:
        print ("Status offline {}".format(res[0]))
    time.sleep(0.5)