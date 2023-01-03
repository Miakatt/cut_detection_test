import tkinter

import serial
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import csv
from tkinter import *
import tkinter.ttk as ttk
import serial.tools.list_ports
import time
'''
Start the ESP8266 unplugged from the board.
Start this script. Connect the ESP8266 to the PCB. 

'''
class ports:
    def __init__(self):
        self.sampleName = ''
        self.com_port = ''

def on_select(event=None):

    # get selection from event
    print("event.widget:", event.widget.get())

    # or get selection directly from combobox
    print("comboboxes: ", cb.get())


def animate(i):
    global x

    y_str = ser.readline()

    y = str(y_str.decode('utf-8'))
    print(y)
    a = int(y[0])
    b = int(y[2])
    c = int(y[4])
    d = int(y[6])
    e = int(y[8])
    f = int(y[10])

    channels = [a, b, c, d, e, f]
    recordData(channels)

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

def recordData(channel):
    stop = datetime.datetime.now()
    stoptime = stop.strftime("%H.%M.%S")
    totaltime = (stop - startTime)

    with open(p.sampleName+".csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([stoptime, totaltime, channel[0], channel[1], channel[2], channel[3], channel[4], channel[5]])
    f.close()
#----------------------------------------------------------

def start():
    p.sampleName = e1.get()
    p.com_port = cb.get()
    startButton['text'] = 'Stop'
    root.quit()
    return p.sampleName, p.com_port


if __name__=="__main__":

    p = ports

    root = Tk()

    root.geometry("250x200")
    frame = Frame(root)

    cb = ttk.Combobox(root, values= serial.tools.list_ports.comports()[0])
    Label(root, text='COM Port').grid(row=0)
    cb.grid(row=0, column=1, padx=10, pady=10)
    cb.bind('<<ComboboxSelected>>', on_select)

    Label(root, text='Save As').grid(row=1)
    e1 = Entry(root)
    e1.grid(row=1, column=1, padx=10, pady=10)

    startButton = tkinter.Button(root, text="Start", width=20, command=start, state='normal')
    startButton.grid(row=2, column=1, padx = 10, pady =10)

    root.mainloop()

    ser = serial.Serial(
        port=p.com_port,  # Set the COM port to whatever it shows in Device Properties.
        baudrate=115200,
        timeout=1)

    max_len = 100
    startTime = datetime.datetime.now()
    print("Start Time: ", startTime.strftime("%H.%M.%S"))
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
