import tkinter as tk
#import win32process
import win32con,win32api,win32gui
import psutil,threading,time,sys
import keyboard

import ctypes as c
from ctypes import wintypes as w

from tkinter import messagebox


class WorldOfGoo(tk.Frame):
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
		self._p = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, self._pid)
		#加载内核模块
		self._md = c.windll.LoadLibrary(r'C:\Windows\System32\kernel32')

		

	def build_gui(self):                    
		# Build GUI
		self.window.title("World Of Goo Cheat ")
		self.window.resizable(width = False, height = False)

		self.window.geometry("300x60") #wxh

		#self.window.option_add('*tearOff', 'FALSE')
		self.grid(column=0, row=0, sticky='ew')

		#------------------Row0--------------------------------------------------
		self.Goo_change = tk.Entry()
		self.Goo_change.grid(row =0,column = 0 )
		self.Goo_change.delete(0, tk.END)
		self.Goo_change.insert(0, 1000)
		tk.Button(text = "Collect Goo" ,anchor = "center" ,width = 20,
				command = self.addGoo).grid(row=0,column=1)

		tk.Label(text = "Press F1 add 1000 Goo", width=40, relief="groove").grid(row=1,column=0,columnspan = 2)


	def start(self):
		keyboard.on_press_key("F1", lambda _:self.addGoo(num = 1000))
		self.window.mainloop()
		

	def addGoo(self, num = 0):
		self.Goo_Mem()
		try:
			if num == 0:
				v = c.c_ulonglong( int(self.Goo_change.get()) + self.Goo() )
			else:
				v = c.c_ulonglong( num + self.Goo() )
			self._md.WriteProcessMemory(int(self._p), c.c_void_p(self.Goo_mem), c.byref(v), c.sizeof(v), None)
			self._md.WriteProcessMemory(int(self._p), c.c_void_p(self.Goo_Cum_Mem), c.byref(v), c.sizeof(v), None)
		
		except Exception as e:
			raise e
			messagebox.showinfo("Error", "Please type a number")
		
		
	def Goo_Mem(self):
		Mem = c.c_ulonglong()
		bytesRead = c.c_ulonglong()
		Base = 0x00007FF7EE39F388

		def prt(*args):
			if len(args) > 0 and type(args[0]) is int:
				print('[{:016X} + {:X}] ->  {:016X}'.format(Base, args[0], Mem.value))
			else:
				print('[{:016X}] ->  {:016X}'.format(Base, Mem.value))

		self._md.ReadProcessMemory(int(self._p), c.c_void_p(Base), c.byref(Mem), c.sizeof(Mem), c.byref(bytesRead))
		#prt()
		Base = Mem.value + 0x18
		self._md.ReadProcessMemory(int(self._p),c.c_void_p(Base),c.byref(Mem),c.sizeof(Mem), c.byref(bytesRead))
		#prt(0x18)
		Base = Mem.value + 0x18
		self._md.ReadProcessMemory(int(self._p),c.c_void_p(Base),c.byref(Mem),c.sizeof(Mem), c.byref(bytesRead))
		#prt(0x18)
		Base = Mem.value + 0x0C0
		self._md.ReadProcessMemory(int(self._p),c.c_void_p(Base),c.byref(Mem),c.sizeof(Mem), c.byref(bytesRead))
		#prt(0x0C0)
		self.Goo_mem = Mem.value + 0x124
		self.Goo_Cum_Mem = Mem.value + 0x110
		#print('[{:016X}] & [{:016X}]'.format(self.Goo, self.Goo_Cum_Mem))

	def Goo(self):
		self.Goo_Mem()

		Goo = c.c_ulonglong()
		self._md.ReadProcessMemory(int(self._p),c.c_void_p(self.Goo_mem),c.byref(Goo),c.sizeof(Goo),None)
		
		if Goo.value > -1:
			return Goo.value

		return 0

	def pid(self):
		pids = psutil.pids()
		for pid in pids:
			p = psutil.Process(pid)# get process name according to pid
			process_name = p.name()
			if 'WorldOfGoo' in process_name:
				return pid

		return -1


'''
25765CF8234 + 110 
25765CF8234 + 124  Ball
第一层偏移
------------------------------------------
2574907DC10 + 0C0 = 25765CF8110 -> 25765CF8234
第二层偏移
------------------------------------------
257476752B0 + 18 = 257476752C8 -> 2574907DC10
第三层偏移
------------------------------------------
WorldOfGoo.exe + 1FF388 = 7FF7EE39F388 + 18 = 25747675970 -> 257476752B0
WorldOfGoo.exe+1FF4F0
WorldOfGoo.exe+1FF648
WorldOfGoo.exe+1FF8F0
WorldOfGoo.exe+1FF908 
基址偏移
------------------------------------------
'''