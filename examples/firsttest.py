from acspy.control import *
import time

if __name__ == "__main__":
    simulator = ACSController("ethernet", 8, "192.168.1.160", 701)
    print(simulator)
    #simulator.disable_all()

    #simulator.enable_all()

    V551bottom = simulator.axes[0]
    V551top = simulator.axes[1]

    print(V551top.disable())
    print(V551top.enable())
    V551top.setVel(10)

    while 1:
        print(V551top.moving)
        print(V551top.ptp(10))
        print(V551top.moving)
        while V551top.moving:
            print(V551top.fpos)
        V551top.ptp(100)
        time.sleep(0.1)
        while V551top.moving:
            print(V551top.fpos)
        print(V551top.fpos)
        break
    print("Done")
