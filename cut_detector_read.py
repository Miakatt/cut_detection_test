import serial
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import csv

def animate(i):
    global x

    y_str = ser.readline()

    y = str(y_str.decode('utf-8'))
    a = int(y[0])
    b = int(y[2])
    c = int(y[4])
    d = int(y[6])
    e = int(y[8])
    f = int(y[10])

    if (a==0):
        stoptimer("1")
    if (b==0):
        stoptimer("2")
    if (c==0):
        stoptimer("3")
    if (d==0):
        stoptimer("4")
    if (e==0):
        stoptimer("5")
    if (f==0):
        stoptimer("6")

    data_a.append((x, a))
    data_b.append((x, b))
    data_c.append((x, c))
    data_d.append((x, d))
    data_e.append((x, e))
    data_f.append((x, f))

    ax.relim()
    ax.autoscale_view()

    line_a.set_data(*zip(*data_a))
    line_b.set_data(*zip(*data_b))
    line_c.set_data(*zip(*data_c))
    line_d.set_data(*zip(*data_d))
    line_e.set_data(*zip(*data_e))
    line_f.set_data(*zip(*data_f))

    x += 0.1

def stoptimer(channel):
    stop = datetime.datetime.now()
    stoptime = stop.strftime("%H.%M.%S")
    totaltime = (stop - startTime)
    print("Channel %s has been cut at %s. Total time to cut: %s" %(channel, stoptime, totaltime))
    with open(sampleName+".csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([stoptime, channel, totaltime])

#----------------------------------------------------------


if __name__=="__main__":
    sampleName = input("ENTER SAMPLE ID:  ")
    max_len = 100
    startTime = datetime.datetime.now()
    print("Start Time: " , startTime.strftime("%H.%M.%S"))
    ser = serial.Serial(
        port='COM5',       # Set the COM port to whatever it shows in Device Properties.
        baudrate=9600,
        timeout=1)

    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(12)
    x = 0
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    data_a = deque([(x, a)], maxlen=max_len)
    data_b = deque([(x, b)], maxlen=max_len)
    data_c = deque([(x, c)], maxlen=max_len)
    data_d = deque([(x, d)], maxlen=max_len)
    data_e = deque([(x, e)], maxlen=max_len)
    data_f = deque([(x, f)], maxlen=max_len)

    line_a, = plt.plot(*zip(*data_a), c='blue')
    line_b, = plt.plot(*zip(*data_b), c='green')
    line_c, = plt.plot(*zip(*data_c), c='red')
    line_d, = plt.plot(*zip(*data_d), c='magenta')
    line_e, = plt.plot(*zip(*data_e), c='cyan')
    line_f, = plt.plot(*zip(*data_f), c='black')
    ani = animation.FuncAnimation(fig, animate, interval=10)
    plt.legend(["ch1", "ch2", "ch3", "ch4", "ch5", "ch6"], loc ="upper left")
    plt.xlabel("Time (s)")
    plt.ylabel("Channel State")
    plt.show()
    