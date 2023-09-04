#!/usr/bin/python
import tkinter as tk
import janus
from functools import partial
import contextlib
with contextlib.redirect_stdout(None):
    from pygame import mixer

class bot_control(tk.Frame):
    def __init__(self, robot, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("J4N-U5 Control Panel")
        self.SCALE_RES = 0.1
        self.H_SCALE_LEN = 500
        self.V_SCALE_LEN = 200
        
        self.robot = robot
        
        self.createWidgets()
                
    def soundboardCallback(self, sound):
        self.robot.playSound(sound)
        
    def eyeSliderCallback(self, cmd):
        self.robot.setMotorCmd('eyes', self.eye_pos.get())
        
    def eyelidSliderCallback(self, cmd):
        self.robot.setMotorCmd('eyelids', self.eyelid_pos.get())
        
    def mouthSliderCallback(self, cmd):
        self.robot.setMotorCmd('mouth', self.mouth_pos.get())
        
    def headYawSliderCallback(self, cmd):
        self.robot.setMotorCmd('head_yaw', self.head_yaw_pos.get())
        
    def personalityCallback(self):
        self.robot.setPersonality(self.personality.get())
        
    def createWidgets(self):
        # head yaw position slider
        self.head_yaw_pos = tk.DoubleVar()
        self.head_yaw_pos.set(self.robot.motors['head_yaw'].init_angle)
        self.head_yaw_scale = tk.Scale(self.master,label="Head Yaw", orient=tk.HORIZONTAL, from_=self.robot.motors['head_yaw'].llim_angle,
                                    to=self.robot.motors['head_yaw'].ulim_angle, variable=self.head_yaw_pos, length=self.H_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.headYawSliderCallback)
        self.head_yaw_scale.grid(column=2, row=0, padx=10, pady=10, columnspan=3)
        
        # eye position slider
        self.eye_pos = tk.DoubleVar()
        self.eye_pos.set(self.robot.motors['eyes'].init_angle)
        self.eye_pos_scale = tk.Scale(self.master,label="Eye Position", orient=tk.HORIZONTAL, from_=self.robot.motors['eyes'].llim_angle,
                                    to=self.robot.motors['eyes'].ulim_angle, variable=self.eye_pos, length=self.H_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.eyeSliderCallback)
        self.eye_pos_scale.grid(column=2, row=1, padx=10, pady=10, columnspan=3)
        
        # eyelid position slider
        self.eyelid_pos = tk.DoubleVar()
        self.eyelid_pos.set(self.robot.motors['eyelids'].init_angle)
        self.eyelid_pos_scale = tk.Scale(self.master,label="Eyelids", orient=tk.VERTICAL, from_=self.robot.motors['eyelids'].llim_angle,
                                    to=self.robot.motors['eyelids'].ulim_angle, variable=self.eyelid_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.eyelidSliderCallback)
        self.eyelid_pos_scale.grid(column=0, row=0, padx=10, pady=10, rowspan=2)
        
        # mouth position slider
        self.mouth_pos = tk.DoubleVar()
        self.mouth_pos.set(self.robot.motors['mouth'].init_angle)
        self.mouth_pos_scale = tk.Scale(self.master,label="Mouth", orient=tk.VERTICAL, from_=self.robot.motors['mouth'].llim_angle,
                                    to=self.robot.motors['mouth'].ulim_angle, variable=self.mouth_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.mouthSliderCallback)
        self.mouth_pos_scale.grid(column=1, row=0, padx=10, pady=10, rowspan=2)
        
        # personality selector
        self.personalityFrame = tk.LabelFrame(self.master, bd=1, text="Personality", padx=10, pady=10)
        self.personalityFrame.grid(column=6, row=0)
        self.personality = tk.IntVar()
        self.personalitysel1 = tk.Radiobutton(self.personalityFrame, text="Good",value=self.robot.GOOD,
                                                variable=self.personality, command=self.personalityCallback)
        self.personalitysel2 = tk.Radiobutton(self.personalityFrame, text="Evil",value=self.robot.EVIL,
                                                variable=self.personality, command=self.personalityCallback)
        self.personalitysel1.grid(column=0,row=0, sticky=tk.W)
        self.personalitysel2.grid(column=0,row=1, sticky=tk.W)
        self.personalitysel1.select()
        self.personalitysel2.deselect()
        
        self.SoundboardFrame = tk.LabelFrame(self.master, bd=1, text="Soundboard")
        self.SoundboardFrame.grid(column=0, row=2, columnspan=3)
        
        self.j = 0
        self.sound_buttons = []
        for i in list(self.robot.sounds):
            self.sound_buttons.append(tk.Button(self.SoundboardFrame,text=i, padx=10, pady=10, command=partial(self.soundboardCallback, sound=i)))
            self.sound_buttons[self.j].grid(column=self.j, row=0, padx=10, pady=10)
            self.j = self.j + 1
    
if __name__ == '__main__':
    robot = janus.janus('calibration.ini', test=False)
    window = bot_control(robot)
    window.mainloop()

