#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import os.path

from PlantsVsZombies.PlantsVsZombies import *
from PlagueInc.PlagueInc import *
from WorldofGoo.WorldOfGoo import *

from tkinter import messagebox
from os import path
from shutil import copyfile

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
		self.window.geometry("300x"+ str(4*30))
		self.window.resizable(width = False, height = False) #fix window size
		global Win
		if not Win:
			messagebox.showinfo("Sorry", "Do not support for Mac")
			exit()

		#--------------------Games-------------------------------------------- 
		tk.Button(self.window, text = "Plants Vs Zombies GOTY",
				command = self.PlantsVsZombies,anchor = tk.W,width = 90).pack()

		tk.Button(self.window, text = "Plague Inc: Evolved 1.17.2",
				command = lambda: self.PlagueInc("1.17.2"),anchor = tk.W,width = 90).pack()

		tk.Button(self.window, text = "Plague Inc: Evolved 1.17.4",
				command = lambda: self.PlagueInc("1.17.4"),anchor = tk.W,width = 90).pack()

		tk.Button(self.window, text = "World Of Goo",
				command = lambda: self.WorldOfgoo(),anchor = tk.W,width = 90).pack()

	def PlagueInc(self,version):
		self.window.destroy()
		PlagueInc(version).start()

	def PlantsVsZombies(self):
		self.window.destroy()
		PVsZ().start()
	
	def WorldOfgoo(self):
		self.window.destroy()
		WorldOfGoo().start()
		
	def start(self):
		self.window.mainloop()

def main():
	com38 = 'C:/Windows/System32/pythoncom38.dll'
	wintype = 'C:/Windows/System32/pywintypes38.dll'
	exist = path.exists(com38) and path.exists(wintype)
	print ("PyWin32 File exists:", exist)
	if not exist:
		source1 = 'pywin32_system32/pythoncom38.dll'
		source2 = 'pywin32_system32/pywintypes38.dll'
		try:
		    copyfile(source1, com38)
		    copyfile(source2, wintype)
		    print("Copied PyWin32 into C/Windows/System32")
		except IOError as e:
		    print("Unable to copy file. %s" % e)
		    exit(1)
		except:
		    print("Unexpected error:", sys.exc_info())
		    exit(1)
	init_window = tk.Tk()
	Cheat_plug = My_Cheat(init_window)
	Cheat_plug.start()

main()