#!/usr/bin/python
import tkinter as tk
from board import SCL, SDA
import busio
from face_motor import *
from eye_color_control import *

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

UPDATE_PERIOD = 20 #MS

class bot_control(tk.Frame):
    def __init__(self, robot, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("J4N-U5 Control Panel")
        self.POS_MIN = 0x0
        self.POS_MAX = 0xFFFF
        self.POS_RESOLUTION = 0x0010
        self.H_SCALE_LEN = 500
        self.V_SCALE_LEN = 200
        self.SCALE_INTERVAL = 45
        
        self.OUTPUT_UPDATE = update
        
        self.robot = robot
        
        self.createWidgets()
        self.master.after(0, self.setOutput)
        
    def createWidgets(self):
        # eye position slider
        self.eyepos = tk.IntVar()
        self.eyepos.set(round((self.POS_MAX - self.POS_MIN) / 2))
        self.eyeposscale = tk.Scale(self.master,label="Eye Position", orient=tk.HORIZONTAL, from_=self.POS_MIN, to=self.POS_MAX, variable=self.eyepos, length=self.H_SCALE_LEN, resolution=self.POS_RESOLUTION)
        self.eyeposscale.grid(column=0, row=1, padx=10, pady=10, columnspan=3)
        
        # eyelid position slider
        self.eyelidpos = tk.IntVar()
        self.eyelidpos.set(self.POS_MAX)
        self.eyelidposscale = tk.Scale(self.master,label="Eyelid Position", orient=tk.VERTICAL, from_=self.POS_MIN, to=self.POS_MAX, variable=self.eyelidpos, length=self.V_SCALE_LEN, resolution=self.POS_RESOLUTION)
        self.eyelidposscale.grid(column=0, row=0, padx=10, pady=10)
        
        # mouth position slider
        self.mouthpos = tk.IntVar()
        self.mouthpos.set(self.POS_MIN)
        self.mouthposscale = tk.Scale(self.master,label="Mouth Position", orient=tk.VERTICAL, from_=self.POS_MIN, to=self.POS_MAX, variable=self.mouthpos, length=self.V_SCALE_LEN, resolution=self.POS_RESOLUTION)
        self.mouthposscale.grid(column=1, row=0, padx=10, pady=10)
        
        
        self.eyeColorFrame = tk.LabelFrame(self.master, bd=1, text="Eye Color", padx=10, pady=10)
        self.eyeColorFrame.grid(column=2, row=0)
        self.eyecolor = tk.IntVar()
        self.eyesel1 = tk.Radiobutton(self.eyeColorFrame, text="Good",value="0", variable=self.eyecolor)
        self.eyesel2 = tk.Radiobutton(self.eyeColorFrame, text="Evil",value="1", variable=self.eyecolor)
        self.eyesel1.grid(column=0,row=0, sticky=tk.W)
        self.eyesel2.grid(column=0,row=1, sticky=tk.W)
        self.eyesel1.select()
        self.eyesel2.deselect()
        
        self.SoundboardFrame = tk.LabelFrame(self.master, bd=1, text="Soundboard")
        self.SoundboardFrame.grid(column=0, row=2, columnspan=3)
        
        self.button1 = tk.Button(self.SoundboardFrame,text="Sound 1", padx=10, pady=10)
        self.button1.grid(column=0,row=0, padx=10, pady=10)
        
        self.button2 = tk.Button(self.SoundboardFrame,text="Sound 2", padx=10, pady=10)
        self.button2.grid(column=1,row=0, padx=10, pady=10)
        
        self.button3 = tk.Button(self.SoundboardFrame,text="Sound 3", padx=10, pady=10)
        self.button3.grid(column=2,row=0, padx=10, pady=10)
        
        self.button4 = tk.Button(self.SoundboardFrame,text="Sound 4", padx=10, pady=10)
        self.button4.grid(column=3,row=0, padx=10, pady=10)

    def setOutput(self):
        if (self.eyecolor.get() == 0):
            self.eye_color.setCmd(0xFFFF, 0, 0xFFFF)
        else:
            self.eye_color.setCmd(0, 0xFFFF, 0xFFFF)
            
        self.eye_move.setCmd(self.eyepos.get())
        self.eyelids.setCmd(self.POS_MAX - self.eyelidpos.get())
        self.mouth.setCmd(self.POS_MAX - self.mouthpos.get())
                
        self.master.after(self.OUTPUT_UPDATE, self.setOutput)
        
    def button1Callback():
        mixer.stop()
        button1sound.play()

    def button2Callback():
        mixer.stop()
        button2sound.play()

    def button3Callback():
        mixer.stop()
        button2sound.play()    

    def button4Callback():
        mixer.stop()
        button2sound.play()
        
i2c_bus = busio.I2C(SCL, SDA)
pca1 = PCA9685(i2c_bus)
pca1.frequency = 50
eye_move = face_motor(pca1, 0, 0, 0xFFFF)
eye_lid = face_motor(pca1, 1, 0, 0xFFFF)
mouth_move = face_motor(pca1, 2, 0, 0xFFFF)
eye_color = eye_color_control(pca1, 4, 5, 6)
window = bot_control(eye_move, eye_color, eye_lid, mouth_move, UPDATE_PERIOD)
window.mainloop()

