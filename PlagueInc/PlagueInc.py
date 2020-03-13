import tkinter as tk
#import win32process
import win32con,win32api,win32gui
import ctypes
import psutil
import threading
import time,sys
import keyboard

from tkinter import messagebox


class PlagueInc(tk.Frame):
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
		self.window.title("Plague Inc Cheat")
		self.window.resizable(width = False, height = False)

		self.window.geometry("300x80") #wxh

		self.window.option_add('*tearOff', 'FALSE')
		self.grid(column=0, row=0, sticky='ew')

		#------------------Row0--------------------------------------------------
		tk.Label(text = "DNA", width=20, relief="groove").grid(row=0,column=0)
		self.dna_label = tk.Label(text = "0", width=20, relief="groove")
		self.dna_label.grid(row=0,column=1)
		
		self.dna_change = tk.Entry()
		self.dna_change.grid(row =1,column = 0 )
		self.dna_change.delete(0, tk.END)
		self.dna_change.insert(0, 1000)
		tk.Button(text = "ADD DNA" ,anchor = "center" ,width = 20,
				command = self.addDNA).grid(row=1,column=1)

		tk.Label(text = "Press F1 add 100 DNA", width=40, relief="groove").grid(row=2,column=0,columnspan = 2)


	def start(self):
		def update():
			while True:
				#time.sleep(2)
				self.dna_label.config(text=self.DNA())


		info_update = threading.Thread(target=update, args=[])
		info_update.daemon = True
		info_update.start()
		keyboard.on_press_key("F1", lambda _:self.addDNA(num = 100))
		self.window.mainloop()
		

	def addDNA(self, num = 0):
		self.DNA_mem()
		try:
			if num == 0:
				v = ctypes.c_long( int(self.dna_change.get()) + self.DNA() )
			else:
				v = ctypes.c_long( num + self.DNA() )
			self._md.WriteProcessMemory(int(self._p), self.DNA_Mem, ctypes.byref(v), 4, None)
			self._md.WriteProcessMemory(int(self._p), self.DNA_Cum_Mem, ctypes.byref(v), 4, None)
		except Exception as e:
			raise e
			messagebox.showinfo("Error", "Please type a number")
		
		

	def DNA_mem(self):
		Mem = ctypes.c_long()  #c语言中的长整形
		#读取内存 + 210
		Base = 0x06EC8938 + 0x210
		self._md.ReadProcessMemory(int(self._p),Base,ctypes.byref(Mem),4,None)
		# -7A40
		Mem1 = Mem.value - 0x7A40
		self._md.ReadProcessMemory(int(self._p),Mem1,ctypes.byref(Mem),4,None)
		# +16C
		Mem1 = Mem.value + 0x16C
		self._md.ReadProcessMemory(int(self._p),Mem1,ctypes.byref(Mem),4,None)
		# +248
		Mem1 = Mem.value + 0x248
		self._md.ReadProcessMemory(int(self._p),Mem1,ctypes.byref(Mem),4,None)
		# +C
		self.DNA_Mem = Mem.value + 0xC
		self.DNA_Cum_Mem = Mem.value + 0x1CC

	def DNA(self):
		self.DNA_mem()

		DNA = ctypes.c_long()
		self._md.ReadProcessMemory(int(self._p),self.DNA_Mem,ctypes.byref(DNA),4,None)
		
		if DNA.value > -1:
			return DNA.value

		return 0

	def pid(self):
		pids = psutil.pids()
		for pid in pids:
			p = psutil.Process(pid)# get process name according to pid
			process_name = p.name()
			if 'PlagueIncEvolved' in process_name:
				return pid

		return -1


'''
add [edx + 1C4],ecx  可能记录累计DNA的数量
ecx = 1 是要增加的数量
eax = 2E 是DNA之后的数量之
edi+04,eax
edi =55C80008
edi = 589C3008
如果放置被检测，需要EDI 和EDI+1C4 一起修改


mov ebp,esp  = ebp = esp
mov edx,[ebp+08] =  edx = [ebp+08]的值
mov eax,[ebp+0C] = eax = [ebp+c] = 0070ED08 + C = 11
mov  ecx,eax    = eax is b(11) ecx = eax = 11
sub ecx,[edx + 04] = ecx - [edx+04] = 1 
add [edx + 1C4],ecx = DNA+1 ,ecx = 1

eax = ebp +8 00070F218
eax + 248

ebp = esp 
[ebp + 08] = edx
[edx + 04] = DNA
[edx +1C4] = DNA_c

mov eax,[eax+0C] 589C3000|589C3AA0

589C3AAC

0508F850-7A40

PlagueExternalMP.dll + 1D128
210
-7A40
06773E10|068D3E10
+16C
+248
+C DNA 的地址
+1CC 为累计DNA 的地址为

22664330 +16C    
24B9E310 +14
26ED8FD4 edx,[eax]
26EEAD9C 
30587444
30587A80    +54
324EEC60	+10 move eax,[26E422F8]
'''