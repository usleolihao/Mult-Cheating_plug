import tkinter as tk
#import win32process,win32con,win32api,win32gui
import ctypes
import psutil
import threading
import time,sys

from tkinter import messagebox


class PVsZ_MAC(tk.Frame):
	# This class defines the graphical user interface 
	def __init__(self, *args, **kwargs):
		#-------------------Basic Windows--------------------------------------
		self.window = tk.Tk()
		tk.Frame.__init__(self, self.window, *args, **kwargs)
		self.build_gui()

		#--------------------Mem-----------------------------------------------
		self._pid = self.pid()

		if self._pid == -1:
			messagebox.showinfo("Error", "Did not find the pid")
			exit()

		#以最高权限打开进程
		#self._p = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, self._pid)
		#加载内核模块
		#self._md = ctypes.windll.LoadLibrary(r'C:\Windows\System32\kernel32')
		

	def build_gui(self):                    
		# Build GUI
		self.window.title("PlantsVsZombies Cheat")
		self.window.resizable(width = False, height = False)

		self.window.geometry("780x240") #wxh
		
		self.window.option_add('*tearOff', 'FALSE')
		self.grid(column=0, row=0, sticky='ew')
		self.grid_columnconfigure(0, weight=1, uniform='a')
		self.grid_columnconfigure(1, weight=1, uniform='a')
		self.grid_columnconfigure(2, weight=1, uniform='a')
		self.grid_columnconfigure(3, weight=1, uniform='a')

		#------------------Row0--------------------------------------------------
		tk.Label(text = "阳光", width=20, relief="groove").grid(row=0,column=0)
		self.sun_label = tk.Label(text = "0", width=20, relief="groove")
		self.sun_label.grid(row=0,column=1)
		
		self.sun_change = tk.Entry()
		self.sun_change.grid(row =0,column = 2 )
		self.sun_change.delete(0, tk.END)
		self.sun_change.insert(0, 1000)
		tk.Button(text = "修改阳光" ,anchor = "center" ,width = 20,
				command = print).grid(row=0,column=3)

		#------------------Row1--------------------------------------------------
		tk.Label(text = "植物1 CD", width=20, relief="groove").grid(row=1,column=0)
		self.cd1_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd1_label.grid(row=1,column=1)
		tk.Label(text = "植物1 CD上限", width=20, relief="groove").grid(row=1,column=2)
		self.cd1u_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd1u_label.grid(row=1,column=3)

		#tk.LabelFrame(text="修改属性").grid(row=2,column=0)
		#tk.Button(self.window, text = name ,anchor = "ne" ,width = 20, command = set_devices).grid(row=i,column=1)
		#------------------Row2--------------------------------------------------
		tk.Label(text = "植物2 CD", width=20, relief="groove").grid(row=2,column=0)
		self.cd2_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd2_label.grid(row=2,column=1)
		tk.Label(text = "植物2 CD上限", width=20, relief="groove").grid(row=2,column=2)
		self.cd2u_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd2u_label.grid(row=2,column=3)
		#------------------Row3--------------------------------------------------
		tk.Label(text = "植物3 CD", width=20, relief="groove").grid(row=3,column=0)
		self.cd3_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd3_label.grid(row=3,column=1)
		tk.Label(text = "植物3 CD上限", width=20, relief="groove").grid(row=3,column=2)
		self.cd3u_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd3u_label.grid(row=3,column=3)
		#------------------Row4--------------------------------------------------
		tk.Label(text = "植物4 CD", width=20, relief="groove").grid(row=4,column=0)
		self.cd4_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd4_label.grid(row=4,column=1)
		tk.Label(text = "植物4 CD上限", width=20, relief="groove").grid(row=4,column=2)
		self.cd4u_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd4u_label.grid(row=4,column=3)
		#------------------Row5--------------------------------------------------
		tk.Label(text = "植物5 CD", width=20, relief="groove").grid(row=5,column=0)
		self.cd5_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd5_label.grid(row=5,column=1)
		tk.Label(text = "植物5 CD上限", width=20, relief="groove").grid(row=5,column=2)
		self.cd5u_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd5u_label.grid(row=5,column=3)
		#------------------Row6--------------------------------------------------
		tk.Label(text = "植物6 CD", width=20, relief="groove").grid(row=6,column=0)
		self.cd6_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd6_label.grid(row=6,column=1)
		tk.Label(text = "植物6 CD上限", width=20, relief="groove").grid(row=6,column=2)
		self.cd6u_label = tk.Label(text = "0", width=20, relief="groove")
		self.cd6u_label.grid(row=6,column=3)

		#------------------Row78--------------------------------------------------
		self.lock_cd1 = tk.BooleanVar()
		self.lock_cd2 = tk.BooleanVar()
		self.lock_cd3 = tk.BooleanVar()
		self.lock_cd4 = tk.BooleanVar()
		self.lock_cd5 = tk.BooleanVar()
		self.lock_cd6 = tk.BooleanVar()
		self.lock_sun = tk.BooleanVar()
		tk.Checkbutton(text="无CD1", var=self.lock_cd1 ).grid(row=7,column=0)
		tk.Checkbutton(text="无CD2", var=self.lock_cd2 ).grid(row=7,column=1)
		tk.Checkbutton(text="无CD3", var=self.lock_cd3 ).grid(row=7,column=2)
		tk.Checkbutton(text="锁定太阳", var=self.lock_sun ).grid(row=7,column=3)
		tk.Checkbutton(text="无CD4", var=self.lock_cd4 ).grid(row=8,column=0)
		tk.Checkbutton(text="无CD5", var=self.lock_cd5 ).grid(row=8,column=1)
		tk.Checkbutton(text="无CD6", var=self.lock_cd6 ).grid(row=8,column=2)


	def start(self):
		#def update():
		#	while True:
		#		#time.sleep(2)
		#		pass

		#info_update = threading.Thread(target=update, args=[])
		#info_update.daemon = True
		#nfo_update.start()
		self.window.mainloop()


	def pid(self):
		pids = psutil.pids()
		for pid in pids:
			p = psutil.Process(pid)# get process name according to pid
			process_name = p.name()
			#print(process_name)
			if 'Plants vs. Zombies' in process_name:
				return pid

		return -1