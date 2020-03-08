import tkinter as tk
import win32process,win32con,win32api,win32gui
import ctypes
import psutil
import threading
import time,sys

from tkinter import messagebox


class PVsZ(tk.Frame):
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
		self._md = ctypes.windll.LoadLibrary(r'C:\Windows\System32\kernel32')
		

	def build_gui(self):                    
		# Build GUI
		self.window.title("PlantsVsZombies Cheat")
		self.window.resizable(width = False, height = False)

		self.window.geometry("580x240") #wxh

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
				command = self.modified_sun).grid(row=0,column=3)

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
		def update():
			while True:
				#time.sleep(2)
				self.sun_label.config(text=self.sun())
				cd = self.cd()
				self.cd1_label.config(text=cd[0])
				self.cd1u_label.config(text=cd[1])
				self.cd2_label.config(text=cd[2])
				self.cd2u_label.config(text=cd[3])
				self.cd3_label.config(text=cd[4])
				self.cd3u_label.config(text=cd[5])
				self.cd4_label.config(text=cd[6])
				self.cd4u_label.config(text=cd[7])
				self.cd5_label.config(text=cd[8])
				self.cd5u_label.config(text=cd[9])
				self.cd6_label.config(text=cd[10])
				self.cd6u_label.config(text=cd[11])
				#self.sun_label['text'] = self.sun()
				self.modified_cd()
				self.LockSun()

		info_update = threading.Thread(target=update, args=[])
		info_update.daemon = True
		info_update.start()
		self.window.mainloop()

	def modified_cd(self):
		v = ctypes.c_long( 1 )
		if self.lock_cd1.get():
			self._md.WriteProcessMemory(int(self._p), self.cd1u_mem, ctypes.byref(v), 4, None)
		if self.lock_cd2.get():
			self._md.WriteProcessMemory(int(self._p), self.cd2u_mem, ctypes.byref(v), 4, None)
		if self.lock_cd3.get():
			self._md.WriteProcessMemory(int(self._p), self.cd3u_mem, ctypes.byref(v), 4, None)
		if self.lock_cd4.get():
			self._md.WriteProcessMemory(int(self._p), self.cd4u_mem, ctypes.byref(v), 4, None)
		if self.lock_cd5.get():
			self._md.WriteProcessMemory(int(self._p), self.cd5u_mem, ctypes.byref(v), 4, None)
		if self.lock_cd6.get():
			self._md.WriteProcessMemory(int(self._p), self.cd6u_mem, ctypes.byref(v), 4, None)

	def LockSun(self):
		if self.lock_sun.get():
			v = ctypes.c_long( int(1000) )
			self._md.WriteProcessMemory(int(self._p), self.sun_ads, ctypes.byref(v), 4, None)

	def modified_sun(self):
		try:
			v = ctypes.c_long( int(self.sun_change.get()) )
			self._md.WriteProcessMemory(int(self._p), self.sun_ads, ctypes.byref(v), 4, None)
		except Exception as e:
			#raise e
			messagebox.showinfo("Error", "Please type a number")
			
	def cd_mem(self):
		cd_Mem = ctypes.c_long()  #c语言中的长整形
		Base = 0x0077959C
		self._md.ReadProcessMemory(int(self._p),Base,ctypes.byref(cd_Mem),4,None)
		cd_Mem1 = cd_Mem.value + 0x868
		self._md.ReadProcessMemory(int(self._p),cd_Mem1,ctypes.byref(cd_Mem),4,None)
		cd_Mem2 = cd_Mem.value + 0x15C
		self._md.ReadProcessMemory(int(self._p),cd_Mem2,ctypes.byref(cd_Mem),4,None)
		self.cd1_mem = cd_Mem.value + 0x4C
		self.cd1u_mem = cd_Mem.value + 0x50
		self.cd2_mem = cd_Mem.value + 0x9C
		self.cd2u_mem = cd_Mem.value + 0xA0
		self.cd3_mem = cd_Mem.value + 0xF0 - 0x4
		self.cd3u_mem = cd_Mem.value + 0xF0 
		self.cd4_mem = cd_Mem.value + 0x140 - 0x4
		self.cd4u_mem = cd_Mem.value + 0x140
		self.cd5_mem = cd_Mem.value + 0x190 - 0x4
		self.cd5u_mem = cd_Mem.value + 0x190
		self.cd6_mem = cd_Mem.value + 0x1E0 - 0x4
		self.cd6u_mem = cd_Mem.value + 0x1E0

	def sun_mem(self):
		Sun_Mem = ctypes.c_long()  #c语言中的长整形
		#读取内存
		Base = 0x007794F8
		self._md.ReadProcessMemory(int(self._p),Base,ctypes.byref(Sun_Mem),4,None)
		# Base + 0x868
		Sun_Mem1 = Sun_Mem.value + 0x868
		self._md.ReadProcessMemory(int(self._p),Sun_Mem1,ctypes.byref(Sun_Mem),4,None)
		# Mem1 + 0x5578 is the Address of the Sun
		Sun_Mem = Sun_Mem.value + 0x5578
		self.sun_ads = Sun_Mem

	def cd(self):
		self.cd_mem()
		cd1 = ctypes.c_long()
		cd1u = ctypes.c_long()
		cd2 = ctypes.c_long()
		cd2u = ctypes.c_long()
		cd3 = ctypes.c_long()
		cd3u = ctypes.c_long()
		cd4 = ctypes.c_long()
		cd4u = ctypes.c_long()
		cd5 = ctypes.c_long()
		cd5u = ctypes.c_long()
		cd6 = ctypes.c_long()
		cd6u = ctypes.c_long()
		self._md.ReadProcessMemory(int(self._p),self.cd1_mem,ctypes.byref(cd1),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd1u_mem,ctypes.byref(cd1u),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd2_mem,ctypes.byref(cd2),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd2u_mem,ctypes.byref(cd2u),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd3_mem,ctypes.byref(cd3),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd3u_mem,ctypes.byref(cd3u),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd1_mem,ctypes.byref(cd4),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd1u_mem,ctypes.byref(cd4u),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd2_mem,ctypes.byref(cd5),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd2u_mem,ctypes.byref(cd5u),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd3_mem,ctypes.byref(cd6),4,None)
		self._md.ReadProcessMemory(int(self._p),self.cd3u_mem,ctypes.byref(cd6u),4,None)
		return [cd1.value,cd1u.value,cd2.value,cd2u.value,cd3.value,cd3u.value,
				cd4.value,cd4u.value,cd5.value,cd5u.value,cd6.value,cd6u.value]


	def sun(self):
		self.sun_mem()
		Sun = ctypes.c_long()
		self._md.ReadProcessMemory(int(self._p),self.sun_ads,ctypes.byref(Sun),4,None)
		return Sun.value

	def pid(self):
		'''
		#找窗体
		#win = win32gui.FindWindow("MainWindow","Plants vs. Zombies GOTY")
		#根据窗体找到进程号
		#hid,pid=win32process.GetWindowThreadProcessId(win)
		'''
		pids = psutil.pids()
		for pid in pids:
			p = psutil.Process(pid)# get process name according to pid
			process_name = p.name()
			if 'PlantsVsZombies' in process_name:
				return pid

		return -1