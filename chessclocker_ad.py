from tkinter import *
import random



class main:
	def __init__(self):
		self.root = Tk()
		self.root.resizable(False, False)
		# self.root.geometry("1000x400")
		self.setup()
		self.place_all()
		self.root.mainloop()

	def setup(self):
		self.is_going = False
		self.is_left = True
		self.is_right = False
		self.bonus = 0 # bonus time every move
	
		self.control_frame = Frame(self.root)
		self.left = 0
		self.right = 0
		
		# is also at the same time pause button!
		self.start_button = Button(self.control_frame, text="start", font=("times", 20), bd=4, activebackground="green", command=self.start)
		self.mode_entry = Entry(self.control_frame, font=("Arial", 15), width=8)
		self.mode_entry.focus_set()
		
		self.left_button = Button(self.control_frame, text="set", font=("Arial", 20), width=2, bd=3, command=self.set_left, activebackground="yellow")
		self.right_button = Button(self.control_frame, text="set", font=("Arial", 20), width=2, bd=3, command=self.set_right, activebackground="yellow")
		
		self.left_timer = Label(self.root, text="00:00", font=("Arial", 80), relief=GROOVE, bd=8, fg="green")
		self.right_timer = Label(self.root, text="00:00", font=("Arial", 80), relief=GROOVE, bd=8)
		
		self.root.bind("<space>", self.start)
		self.root.bind("<KeyPress-Shift_L>", self.switch_right)
		self.root.bind("<KeyPress-Shift_R>", self.switch_left)
		
		
	
	def place_all(self):
		self.control_frame.pack(side=BOTTOM, pady=5)
		
		self.left_timer.pack(side=LEFT, padx=5)
		self.right_timer.pack(side=RIGHT, padx=5)
		
		self.left_button.pack(side=LEFT, padx=50)
		self.right_button.pack(side=RIGHT, padx=50)
		
		self.start_button.pack(pady=10)
		
		Label(self.control_frame, text="mode:", font=("Arial", 15)).pack(side=LEFT, pady=20)
		self.mode_entry.pack(padx=5, side=LEFT)
		Button(self.control_frame, text="config", font=("Arial", 15), command=self.config_mode).pack(side=RIGHT)
		
	def start(self, event=None):
		if self.is_going:
			self.is_going = False
		else:
			if self.right != 0 and self.left != 0:
				self.is_going = True
			
		if self.is_going:
			self.start_button["text"] = "pause"
			self.start_button["activebackground"] = "red"
			self.run()
			self.root.focus_set()

		else:
			self.start_button["text"] = "continue"
			self.start_button["activebackground"] = "green"
		
		
	def run(self):
		if self.is_going:
		    if self.is_left and self.left > 0:
		        self.left -= 0.1
		        self.set_left_str()
		        
		    elif self.is_right and self.right > 0:
		        self.right -= 0.1
		        self.set_right_str()
		        
		    if self.left <= 0:
		        self.left_timer.config(fg="red")
		        self.is_going = False
		        
		    elif self.right <= 0:
		        self.right_timer.config(fg="red")
		        self.is_going = False

		    self.root.after(100, self.run)
	
	def set_left(self):
		self.left_button["text"] = "ok"
		self.left_button["command"] = self.config_left
		self.left_entry = Entry(self.root, width=15)
		self.left_entry.focus_set()
		self.left_entry.place(x=60, y=170)
		
		# left min. label
		self.left_min = Label(self.root, text="min.")
		self.left_min.place(x=240, y=170)
	
	def config_left(self):
		time = self.left_entry.get()
		if time:
			self.left = float(time) * 60
			self.set_left_str()
		
		self.left_entry.place_forget()
		self.left_min.place_forget()
		self.left_button["text"] = "set"
		self.left_button["command"] = self.set_left
		
	def set_right(self):
		self.right_button["text"] = "ok"
		self.right_button["command"] = self.config_right
		self.right_entry = Entry(self.root, width=15)
		self.right_entry.focus_set()
		self.right_entry.place(x=460, y=170)
		
		# right min. label
		self.right_min = Label(self.root, text="min.")
		self.right_min.place(x=645, y=170)
	
	def config_right(self):
		time = self.right_entry.get()
		if time:
			self.right = float(time) * 60
			self.set_right_str()
		
		self.right_entry.place_forget()
		self.right_min.place_forget()
		self.right_button["text"] = "set"
		self.right_button["command"] = self.set_right
		
	def time_format(self, time):
		s = ""
		min = time / 60
		sec = time % 60
		if min < 10:	
			s = "0" + str(int(min)) + ":" + str(int(sec))
			if sec < 10:
				s = "0" + str(int(min)) + ":0" + str(int(sec))
		else:
			s = str(int(min)) + ":" + str(int(sec))
			if sec < 10:
				s = str(int(min)) + ":0" + str(int(sec))
		
		return s
		
	def set_left_str(self):
		self.left_timer["text"] = self.time_format(self.left)
	
	def set_right_str(self):
		self.right_timer["text"] = self.time_format(self.right)
		
	def switch_right(self, event=None):
		if self.is_left:
			self.left += self.bonus
			self.right_timer["fg"] = "green"
			self.left_timer["fg"] = "black"
			self.is_left = False
			self.is_right = True
		
		self.set_left_str()
	
	def switch_left(self, event=None):
		if self.is_right:
			self.right += self.bonus
			self.left_timer["fg"] = "green"
			self.right_timer["fg"] = "black"
			self.is_left = True
			self.is_right = False
			
		self.set_right_str()
			
	def config_mode(self, event=None):
		mode = self.mode_entry.get()
		try:
			l = mode.split("+")
			self.right = float(l[0]) * 60
			self.left = float(l[0]) * 60
			self.bonus = int(l[1])
		except:
			pass
		self.set_right_str()
		self.set_left_str()
		self.root.focus_set()
		
		
			

if __name__ == '__main__':
    main()
