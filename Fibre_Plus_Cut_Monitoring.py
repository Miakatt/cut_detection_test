import tkinter
import serial
import datetime
import csv
from tkinter import *
import tkinter.ttk as ttk
import serial.tools.list_ports
import time
import PySimpleGUI as sg
import numpy as np

'''
Start the ESP8266 unplugged from the board.
Start this script. Connect the ESP8266 to the PCB. 

'''
#==============================================================
sg.theme('Light Grey 6')

CIRCLE = '⚫'
CROSS = '❌'

layout = [  [sg.Text('Channel 1  '), sg.Text(CROSS, text_color='green', key='-LED0-')],
            [sg.Text('Channel 2  '), sg.Text(CROSS, text_color='green', key='-LED1-')],
            [sg.Text('Channel 3  '), sg.Text(CROSS, text_color='green', key='-LED2-')],
            [sg.Text('Channel 4  '), sg.Text(CROSS, text_color='green', key='-LED3-')],
            [sg.Text('Channel 5  '), sg.Text(CROSS, text_color='green', key='-LED4-')],

            [sg.Button('Exit')]]

window = sg.Window('Fiber+ Cut Monitoring', layout, font='Any 16')

#==============================================================
class ports:
    def __init__(self):
        self.sampleName = ''
        self.com_port = ''
#==============================================================
def on_select(event=None):

    # get selection from event
    print("event.widget:", event.widget.get())

    # or get selection directly from combobox
    print("comboboxes: ", cb.get())
#==============================================================

def recordData(channel):
    stop = datetime.datetime.now()
    stoptime = stop.strftime("%H:%M:%S.%f").strip()[:-4]
    totaltime = (stop - startTime)

    with open(p.sampleName+".csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([stoptime, totaltime, channel[0], channel[1], channel[2], channel[3], channel[4]])
    f.close()
    return totaltime
#==============================================================

def start():
    p.sampleName = e1.get()
    p.com_port = cb.get()
    startButton['text'] = 'Stop'
    root.quit()
    return p.sampleName, p.com_port

#==============================================================


def start():
    p.sampleName = e1.get()
    p.com_port = cb.get()
    startButton['text'] = 'Stop'
    root.quit()
    return p.sampleName, p.com_port
#==============================================================
#==============================================================

if __name__ == "__main__":

    p = ports
    root = Tk()
    # open window to select COM Port
    root.geometry("250x200")
    frame = Frame(root)
    # Provide pulldown list of selectable COM Ports
    cb = ttk.Combobox(root, values= serial.tools.list_ports.comports()[0])
    Label(root, text='COM Port').grid(row=0)
    cb.grid(row=0, column=1, padx=10, pady=10)
    cb.bind('<<ComboboxSelected>>', on_select)
    # Save data as.
    Label(root, text='Save As').grid(row=1)
    e1 = Entry(root)
    e1.grid(row=1, column=1, padx=10, pady=10)
    startButton = tkinter.Button(root, text="Start", width=20, command=start, state='normal')
    startButton.grid(row=2, column=1, padx = 10, pady =10)

    root.mainloop()
    # Set up Serial Communication with ESP8266
    ser = serial.Serial(
        port=p.com_port,  # Set the COM port to whatever it shows in Device Properties.
        baudrate=115200,
        timeout=1)
    time.sleep(0.1)
    startTime = datetime.datetime.now()
    print("Start Time: ", startTime.strftime("%H.%M.%S"))
    #Clear Serial Buffer
    ser.flush()
    while True:
        ser.flush()
        # read the status of the current layout
        event, values = window.read(timeout=10)
        # read data waiting at the serial port
        while ser.in_waiting:
            y_str = ser.readline()
            print(y_str)
            y = str(y_str.decode('utf-8'))

            # split data in to the 6 channels
            a = int(y[0])
            b = int(y[2])
            c = int(y[4])
            d = int(y[6])
            e = int(y[8])

            channels = [a, b, c, d, e]
            # store data to CSV
            cut_time = recordData(channels)
            # Scan data values and update the GUI
            for i in range(0, 5):
                if channels[i]<1:
                    window[f'-LED{i}-'].update(CIRCLE)
                else:
                    window[f'-LED{i}-'].update(CROSS)
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            # write the last row as zeros.
            channels = [0, 0, 0, 0, 0]
            recordData(channels)
            break
    window.close()
