#!/usr/bin/python
import tkinter as tk
from board import SCL, SDA
import busio
import janus
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

UPDATE_PERIOD = 20 #MS

class bot_control(tk.Frame):
    def __init__(self, robot, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("J4N-U5 Control Panel")
        self.POS_MIN = 0x0
        self.POS_MAX = 0xFFFF
        self.POS_RESOLUTION = 0.1
        self.H_SCALE_LEN = 500
        self.V_SCALE_LEN = 200
        self.SCALE_INTERVAL = 45
        
        self.robot = robot
        
        self.createWidgets()
        self.master.after(0, self.setOutput)
        
    def setOutput(self):
        self.robot.update()                
        self.master.after(self.robot.getRate(), self.setOutput)
        
    def button1Callback(self):
        self.mixer.stop()
        self.button1sound.play()

    def button2Callback(self):
        self.mixer.stop()
        self.button2sound.play()

    def button3Callback(self):
        self.mixer.stop()
        self.button2sound.play(self)    

    def button4Callback(self):
        self.ixer.stop()
        self.button2sound.play(self)
        
    def eyeMoveSliderCallback(self, cmd):
        self.robot.setEyePositionCmd(self.eyepos.get())
        
    def eyeLidSliderCallback(self, cmd):
        self.robot.setEyeLidPositionCmd(self.eyelidpos.get())
        
    def mouthMoveSliderCallback(self, cmd):
        self.robot.setMouthPositionCmd(self.mouthpos.get())
        
    def headYawSliderCallback(self, cmd):
        self.robot.setHeadYawPositionCmd(self.head_yawpos.get())
        
    def headRollSliderCallback(self, cmd):
        self.robot.setHeadRollPositionCmd(self.head_rollpos.get())
        
    def eyeColorCallback(self):
        if (self.eyecolor.get() == 0):
            self.robot.setEyeColor(self.robot.eye_light.llim, self.robot.eye_light.ulim, self.robot.eye_light.llim)
        else:
            self.robot.setEyeColor(self.robot.eye_light.ulim, self.robot.eye_light.llim, self.robot.eye_light.llim)
        
    def mouthColorUpdate(self):
        self.robot.setEyeColor(r_cmd, g_cmd, b_cmd)
        
    def createWidgets(self):
        # eye position slider
        self.eyepos = tk.DoubleVar()
        self.eyepos.set(round((self.POS_MAX - self.POS_MIN) / 2))
        self.eyeposscale = tk.Scale(self.master,label="Eye Position", orient=tk.HORIZONTAL, from_=self.robot.eye_move_langle, to=self.robot.eye_move_uangle, variable=self.eyepos, length=self.H_SCALE_LEN, resolution=self.POS_RESOLUTION, command=self.eyeMoveSliderCallback)
        self.eyeposscale.grid(column=0, row=1, padx=10, pady=10, columnspan=3)
        self.eyepos.set((self.robot.eye_move_uangle + self.robot.eye_move_langle) / 2)
        self.robot.setEyePositionCmd(self.eyepos.get())
        
        # eyelid position slider
        self.eyelidpos = tk.DoubleVar()
        self.eyelidpos.set(self.POS_MAX)
        self.eyelidposscale = tk.Scale(self.master,label="Eyelid Position", orient=tk.VERTICAL, from_=self.robot.eyelid_move_langle, to=self.robot.eyelid_move_uangle, variable=self.eyelidpos, length=self.V_SCALE_LEN, resolution=self.POS_RESOLUTION, command=self.eyeLidSliderCallback)
        self.eyelidposscale.grid(column=0, row=0, padx=10, pady=10)
        self.eyelidpos.set((self.robot.eyelid_move_uangle + self.robot.eyelid_move_langle) / 2)
        self.robot.setEyeLidPositionCmd(self.eyelidpos.get())
        
        # mouth position slider
        self.mouthpos = tk.DoubleVar()
        self.mouthpos.set(self.POS_MAX)
        self.mouthposscale = tk.Scale(self.master,label="Mouth Position", orient=tk.VERTICAL, from_=self.robot.mouth_move_langle, to=self.robot.mouth_move_uangle, variable=self.mouthpos, length=self.V_SCALE_LEN, resolution=self.POS_RESOLUTION, command=self.mouthMoveSliderCallback)
        self.mouthposscale.grid(column=1, row=0, padx=10, pady=10)
        self.mouthpos.set((self.robot.mouth_move_uangle + self.robot.mouth_move_langle) / 2)
        self.robot.setMouthPositionCmd(self.mouthpos.get())
        
        # head yaw position slider
        self.head_yawpos = tk.DoubleVar()
        self.head_yawpos.set(self.POS_MAX)
        self.head_yawposscale = tk.Scale(self.master,label="head Yaw Position", orient=tk.VERTICAL, from_=self.robot.head_yaw_move_langle, to=self.robot.head_yaw_move_uangle, variable=self.head_yawpos, length=self.V_SCALE_LEN, resolution=self.POS_RESOLUTION, command=self.headYawSliderCallback)
        self.head_yawposscale.grid(column=2, row=0, padx=10, pady=10)
        self.head_yawpos.set((self.robot.head_yaw_move_uangle + self.robot.head_yaw_move_langle) / 2)
        self.robot.setHeadYawPositionCmd(self.head_yawpos.get())
        
        # head Roll position slider
        self.head_rollpos = tk.DoubleVar()
        self.head_rollpos.set(self.POS_MAX)
        self.head_rollposscale = tk.Scale(self.master,label="Head Roll Position", orient=tk.VERTICAL, from_=self.robot.head_roll_move_langle, to=self.robot.head_roll_move_uangle, variable=self.head_rollpos, length=self.V_SCALE_LEN, resolution=self.POS_RESOLUTION, command=self.headRollSliderCallback)
        self.head_rollposscale.grid(column=3, row=0, padx=10, pady=10)
        self.head_rollpos.set((self.robot.head_roll_move_uangle + self.robot.head_roll_move_langle) / 2)
        self.robot.setHeadRollPositionCmd(self.head_rollpos.get())
        
        self.eyeColorFrame = tk.LabelFrame(self.master, bd=1, text="Eye Color", padx=10, pady=10)
        self.eyeColorFrame.grid(column=4, row=0)
        self.eyecolor = tk.IntVar()
        self.eyesel1 = tk.Radiobutton(self.eyeColorFrame, text="Good",value="0", variable=self.eyecolor, command=self.eyeColorCallback)
        self.eyesel2 = tk.Radiobutton(self.eyeColorFrame, text="Evil",value="1", variable=self.eyecolor, command=self.eyeColorCallback)
        self.eyesel1.grid(column=0,row=0, sticky=tk.W)
        self.eyesel2.grid(column=0,row=1, sticky=tk.W)
        self.eyesel1.select()
        self.eyesel2.deselect()
        self.robot.setEyeColor(self.robot.eye_light.llim, self.robot.eye_light.ulim, self.robot.eye_light.llim)
        
        self.SoundboardFrame = tk.LabelFrame(self.master, bd=1, text="Soundboard")
        self.SoundboardFrame.grid(column=0, row=2, columnspan=3)
        
        self.button1 = tk.Button(self.SoundboardFrame,text="Sound 1", padx=10, pady=10, command=self.button1Callback)
        self.button1.grid(column=0,row=0, padx=10, pady=10)
        
        self.button2 = tk.Button(self.SoundboardFrame,text="Sound 2", padx=10, pady=10, command=self.button2Callback)
        self.button2.grid(column=1,row=0, padx=10, pady=10)
        
        self.button3 = tk.Button(self.SoundboardFrame,text="Sound 3", padx=10, pady=10, command=self.button3Callback)
        self.button3.grid(column=2,row=0, padx=10, pady=10)
        
        self.button4 = tk.Button(self.SoundboardFrame,text="Sound 4", padx=10, pady=10, command=self.button4Callback)
        self.button4.grid(column=3,row=0, padx=10, pady=10)
    
robot = janus.janus('calibration.ini')
window = bot_control(robot)
window.mainloop()

