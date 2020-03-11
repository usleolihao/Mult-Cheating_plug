import tkinter as tk
#import win32process
import win32con,win32api,win32gui
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

		self.window.geometry("580x380") #wxh

		self.window.option_add('*tearOff', 'FALSE')
		self.grid(column=0, row=0, sticky='ew')

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

		#------------------Row1-10--------------------------------------------------
		
		self.cd_label = list()
		self.cdu_label = list()
		self.lock_cd = list()

		for i in range(1,11):
			t1 = "植物"+str(i) +" CD"
			tk.Label(text = t1, width=20, relief="groove").grid(row=i,column=0)
			cd_label = tk.Label(text = "0", width=20, relief="groove")
			cd_label.grid(row=i,column=1)
			tk.Label(text = t1 + "上限", width=20, relief="groove").grid(row=i,column=2)
			cdu_label = tk.Label(text = "0", width=20, relief="groove")
			cdu_label.grid(row=i,column=3)
			self.cd_label.append(cd_label)
			self.cdu_label.append(cdu_label)
			self.lock_cd.append(tk.BooleanVar())

		#------------------Row111213--------------------------------------------------
		self.lock_sun = tk.BooleanVar()
		for i in range(10):
			row = int(i/4)
			tk.Checkbutton(text="无CD"+str(i+1), var=self.lock_cd[i] ).grid(row=11 + row,column=i%4)

		tk.Checkbutton(text="锁定阳光", var=self.lock_sun ).grid(row=13,column=2)

		#------------------Row14--------------------------------------------------
		tk.Label(text = "添加金币 *10", width=20, relief="groove").grid(row=14,column=0)
		self.money = tk.Entry()
		self.money.grid(row =14,column = 1 )
		self.money.delete(0, tk.END)
		self.money.insert(0, 100)
		tk.Button(text = "添加" ,anchor = "center" ,width = 20,
				command = self.modified_money).grid(row=14,column=2)

	def start(self):
		def update():
			while True:
				#time.sleep(2)
				self.sun_label.config(text=self.sun())
				self.cd()
				for i in range(10):
					self.cd_label[i].config(text = self._cd[i][0])
					self.cdu_label[i].config(text = self._cd[i][1])

				self.modified_cd()
				self.LockSun()

		info_update = threading.Thread(target=update, args=[])
		info_update.daemon = True
		info_update.start()
		self.window.mainloop()

	def modified_cd(self):
		v = ctypes.c_long( 1 )
		for i in range(10):
			if self.lock_cd[i].get():
				self._md.WriteProcessMemory(int(self._p), self.cdu_mem[i], ctypes.byref(v), 4, None)

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
	
	def modified_money(self):
		try:
			Mem = ctypes.c_long()  #c语言中的长整形
			#读取内存
			Base = 0x007794F8
			self._md.ReadProcessMemory(int(self._p),Base,ctypes.byref(Mem),4,None)
			# Base + 0x950
			Mem1 = Mem.value + 0x950
			self._md.ReadProcessMemory(int(self._p),Mem1,ctypes.byref(Mem),4,None)
			# Mem1 + 0x50 is the Address of the Sun
			Mem = Mem.value + 0x50

			v = ctypes.c_long()
			self._md.ReadProcessMemory(int(self._p),Mem,ctypes.byref(v),4,None)
			v = ctypes.c_long(int(self.money.get()) + v.value) 

			self._md.WriteProcessMemory(int(self._p), Mem, ctypes.byref(v), 4, None)
		except Exception as e:
			raise e
			messagebox.showinfo("Error", "Please type a number")		

	def get_cd_mem(self):
		self.cd_mem = list()
		self.cdu_mem = list()
		cd_Mem = ctypes.c_long()  #c语言中的长整形
		Base = 0x0077959C
		self._md.ReadProcessMemory(int(self._p),Base,ctypes.byref(cd_Mem),4,None)
		cd_Mem1 = cd_Mem.value + 0x868
		self._md.ReadProcessMemory(int(self._p),cd_Mem1,ctypes.byref(cd_Mem),4,None)
		cd_Mem2 = cd_Mem.value + 0x15C
		self._md.ReadProcessMemory(int(self._p),cd_Mem2,ctypes.byref(cd_Mem),4,None)
		for i in range(10):
			self.cd_mem.append(cd_Mem.value + (i+1)*(0x4C))
			self.cdu_mem.append(cd_Mem.value + (i+1)*(0x50))


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
		self._cd = list()
		self.get_cd_mem()
		cd = list()
		cdu = list()

		for i in range(10):
			cd.append(ctypes.c_long())
			cdu.append(ctypes.c_long())
			self._md.ReadProcessMemory(int(self._p),self.cd_mem[i],ctypes.byref(cd[i]),4,None)
			self._md.ReadProcessMemory(int(self._p),self.cdu_mem[i],ctypes.byref(cdu[i]),4,None)
			self._cd.append((cd[i].value,cdu[i].value))

	def sun(self):
		self.sun_mem()
		Sun = ctypes.c_long()
		self._md.ReadProcessMemory(int(self._p),self.sun_ads,ctypes.byref(Sun),4,None)
		return Sun.value

	def pid(self):
		'''
		#找窗体 win = win32gui.FindWindow("MainWindow","Plants vs. Zombies GOTY")
		#根据窗体找到进程号 hid,pid=win32process.GetWindowThreadProcessId(win)
		'''
		pids = psutil.pids()
		for pid in pids:
			p = psutil.Process(pid)# get process name according to pid
			process_name = p.name()
			if 'PlantsVsZombies' in process_name:
				return pid

		return -1