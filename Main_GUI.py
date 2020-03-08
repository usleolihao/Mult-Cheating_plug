#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from PlantsVsZombies.PlantsVsZombies import *
from tkinter import messagebox

def get_platform():
	platforms = {
		'linux1' : 'Linux',
		'linux2' : 'Linux',
		'darwin' : 'OS X',
		'win32' : 'Windows'
	}
	if sys.platform not in platforms:
		return sys.platform
	
	return platforms[sys.platform]

global Win
Win = True if get_platform() == 'Windows' else False

class My_Cheat(tk.Frame):

	def __init__(self, window, *args, **kwargs):
		tk.Frame.__init__(self, window, *args, **kwargs)
		#--------------------Windows-----------------------------------------
		self.window = window
		self.window.title("Cheat_plug")
		self.window.geometry("300x"+ str(1*30))
		self.window.resizable(width = False, height = False) #fix window size

		#--------------------Games-------------------------------------------- 
		tk.Button(self.window, text = "PlantsVsZombies",
				command = self.PlantsVsZombies,anchor = tk.W,width = 90).pack()

	def PlantsVsZombies(self):
		self.window.destroy()
		global Win

		if Win:
			PVsZ().start()
		else:
			messagebox.showinfo("Sorry", "Do not support for Mac")
			exit()

		
	def start(self):
		self.window.mainloop()

def main():
	init_window = tk.Tk()
	Cheat_plug = My_Cheat(init_window)
	Cheat_plug.start()

main()