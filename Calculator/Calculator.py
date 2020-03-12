#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from tkinter import messagebox

class Calculator(tk.Frame):

	def __init__(self, window, *args, **kwargs):
		tk.Frame.__init__(self, window, *args, **kwargs)
		#--------------------Windows-----------------------------------------
		scale = ['Hex',
				'Decimal',
				'octal',
				'binary']

		self.window = window
		self.window.title("Calculator")
		self.window.geometry("360x"+ str(len(scale)*36))
		self.window.resizable(width = False, height = False) #fix window size

		self.scale = tk.IntVar()
		self.A = list()
		self.B = list()
		self.Ans_Label = list()

		

		for i in range(len(scale)):
			tk.Radiobutton(text = scale[i], value=i, var=self.scale).grid(row=i,column=0)
			self.A.append(tk.Entry(width = 10))
			self.B.append(tk.Entry(width = 10))
			self.A[i].grid(row = i,column = 1 )
			self.B[i].grid(row = i,column = 2 )
			ans = tk.Label(text = "Ans:", width=20, relief="groove")
			ans.grid(row= i,column=3)
			self.Ans_Label.append(ans)

		self.choice = tk.IntVar()
		tk.Radiobutton(text = 'add', value=0, var=self.choice).grid(row=len(scale) + 1,column=1)
		tk.Radiobutton(text = 'sub', value=1, var=self.choice).grid(row=len(scale) + 1,column=2)
		tk.Button(text = 'result', command = self.Calulate).grid(row=len(scale) + 1,column=3)
	
	def start(self):
		self.window.mainloop()

	def Calulate(self):
		scale = self.scale.get()
		op = self.choice.get()

		scalor = [16,10,8,2]

		num1 = self.A[scale].get()
		num2 = self.B[scale].get()
		Ans = -1
		#-----convert into right scale
		try:
			transnum = scalor[scale]
			num1 = int(num1,transnum)
			num2 = int(num2,transnum)
		except Exception as e:
			messagebox.showinfo("Error", "Please select correct type")
			return

		if op == 0:
			Ans = num1 + num2
		elif op == 1:
			Ans = num1 - num2

		#now we get ans in decimal (num1,num2,ans) in 10 base
		for i in range(len(scalor)):
			self.A[i].delete(0, tk.END)
			self.B[i].delete(0, tk.END)

		self.A[0].insert(0, hex(num1))
		self.A[1].insert(0, str(num1))
		self.A[2].insert(0, oct(num1))
		self.A[3].insert(0, bin(num1))
		self.B[0].insert(0, hex(num2))
		self.B[1].insert(0, str(num2))
		self.B[2].insert(0, oct(num2))
		self.B[3].insert(0, bin(num2))
		self.Ans_Label[0]['text'] = 'Ans: ' + hex(Ans)
		self.Ans_Label[1]['text'] = 'Ans: ' + str(Ans)
		self.Ans_Label[2]['text'] = 'Ans: ' + oct(Ans)
		self.Ans_Label[3]['text'] = 'Ans: ' + bin(Ans)

Calculator(tk.Tk()).start()