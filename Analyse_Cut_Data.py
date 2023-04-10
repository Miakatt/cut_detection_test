import pandas as pd
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime
import numpy as np

def get_data_path():
	# Assumes using Python3.
	# Opens a dialog window for selecting the csv file.
	if sys.version_info[0] == 3:
		print ('Python 3.x installed')
		import tkinter as tk
		from tkinter import filedialog as fd
		time.sleep(0.1)
		root = tk.Tk()
		root.withdraw()
		print ("SELECT INPUT TDMS FILE.\n")
		file_path = fd.askopenfilename \
			(initialdir=r'C:\Users\admin\OneDrive - Bekaert\Python Codes\Cut Detection',
									   title="Select CSV file",
									   filetypes=[("csv files", ".csv")]
									   )
		time.sleep(0.1)
		root.withdraw()
		return file_path
	else:
		print("Sorry. This requires python 3. Get with the times!")


if __name__=="__main__":
	filename = get_data_path()
	print(filename)
	columns = (['real_time', 'elapsed_time', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5'])
	df = pd.read_csv(filename, names=columns, sep=',')
	print(df['real_time'])
	fig, ax = plt.subplots(1,1)
	fig.set_figheight(5)
	fig.set_figwidth(15)
	ax.plot(df['elapsed_time'], df['ch1'], 'r', label='ch1')
	ax.plot(df['elapsed_time'], df['ch2'], 'g', label='ch2')
	ax.plot(df['elapsed_time'], df['ch3'], 'b', label='ch3')
	ax.plot(df['elapsed_time'], df['ch4'], 'm', label='ch4')
	ax.plot(df['elapsed_time'], df['ch5'], 'k', label='ch5')
	ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
	plt.legend()
	plt.draw()
	plt.pause(0.01)

	cut_times = []
	for i in range(2, 7):
		cut_time_index = df[df.iloc[:,i] == 0].index[0]
		cut_times.append(datetime.strptime(df['elapsed_time'][cut_time_index], '%H:%M:%S.%f'))

	cut_times.sort()
	print(cut_times[1])
	print(cut_times[0])
	print("Cut through time : ", (cut_times[1] - cut_times[0]))
	# print(df['elapsed_time'][cut_times[1]]) # - df['elapsed_time'][cut_times[0]]
	# #print("Cut Through Time:  %3.1f seconds" % CTT )

	plt.show()