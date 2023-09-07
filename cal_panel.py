#!/usr/bin/python
import tkinter as tk
from lib.janus import janus
from functools import partial
import contextlib
with contextlib.redirect_stdout(None):
    from pygame import mixer

# import scripts
from scripts import welcomeScript

class cal_panel(tk.Frame):
    def __init__(self, robot, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("J4N-U5 Calibration Panel")
        self.SCALE_RES = 0.1
        self.H_SCALE_LEN = 200
        self.V_SCALE_LEN = 200
        
        self.winfo_toplevel().protocol('WM_DELETE_WINDOW', self.on_close)
        self.robot = robot
        
        self.createWidgets()
        
        
                
    def motorPositionSliderCallback(self, cmd, motor):
        self.robot.setMotorCmd(motor, float(cmd))
        
    def motorRateSliderCallback(self, cmd, motor):
        self.robot.motors[motor].setRate(int(cmd))
        
    def colorCallback(self, cmd):
        self.robot.setLightCmd((self.red_pos.get(),self.green_pos.get(),self.blue_pos.get()))
        
    def fadeRateCallback(self, cmd):
        self.robot.setCrossfadeRate(float(cmd))
    
    def soundboardCallback(self, sound):
        self.robot.playSound(sound)
        
    def scriptWelcomeCallback(self):
        for i in self.controls:
            self.controls[i]['state'] = tk.DISABLED
            
        welcomeScript.welcomeScript(self.robot)
        
        for i in self.controls:
            self.controls[i]['state'] = tk.NORMAL
        
    def createWidgets(self):
        
        self.controls = dict()
        # Eyelid Panel
        self.eyelid_frame = tk.LabelFrame(self.master, bd=1, text="Eyelids")
        self.eyelid_frame.grid(column=0, row=0)
        
        # eyelid position slider
        self.eyelid_pos = tk.DoubleVar()
        self.eyelid_pos.set(self.robot.motors['eyelids'].init_angle)
        self.controls['eyelid_pos'] = tk.Scale(self.eyelid_frame,label="Eyelids", orient=tk.VERTICAL, from_=self.robot.motors['eyelids'].llim_angle,
                                    to=self.robot.motors['eyelids'].ulim_angle, variable=self.eyelid_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.motorPositionSliderCallback, motor='eyelids'))
        self.controls['eyelid_pos'].grid(column=0, row=0, padx=10, pady=10, rowspan=3)
        
        # eyelid rate slider
        self.eyelid_rate = tk.DoubleVar()
        self.eyelid_rate.set(self.robot.motors['eyelids'].rate)
        self.controls['eyelid_rate'] = tk.Scale(self.eyelid_frame,label="Eyelid Rate", orient=tk.VERTICAL, from_=360,
                                    to=0, variable=self.eyelid_rate, length=self.V_SCALE_LEN,
                                    resolution=1, command=partial(self.motorRateSliderCallback, motor='eyelids'))
        self.controls['eyelid_rate'].grid(column=1, row=0, padx=10, pady=10, rowspan=3)
        
        #Set buttons
        
        # Mouth Panel
        self.mouth_frame = tk.LabelFrame(self.master, bd=1, text="Mouth")
        self.mouth_frame.grid(column=1, row=0)
        
        # mouth position slider
        self.mouth_pos = tk.DoubleVar()
        self.mouth_pos.set(self.robot.motors['mouth'].init_angle)
        self.controls['mouth_pos'] = tk.Scale(self.mouth_frame,label="Mouth", orient=tk.VERTICAL, from_=self.robot.motors['mouth'].llim_angle,
                                    to=self.robot.motors['mouth'].ulim_angle, variable=self.mouth_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.motorPositionSliderCallback, motor='mouth'))
        self.controls['mouth_pos'].grid(column=0, row=0, padx=10, pady=10, rowspan=3)
        
        # mouth Rate slider
        self.mouth_rate = tk.DoubleVar()
        self.mouth_rate.set(self.robot.motors['mouth'].rate)
        self.controls['mouth_rate'] = tk.Scale(self.mouth_frame,label="Mouth Rate", orient=tk.VERTICAL, from_=360,
                                    to=0, variable=self.mouth_rate, length=self.V_SCALE_LEN,
                                    resolution=1, command=partial(self.motorRateSliderCallback, motor='mouth'))
        self.controls['mouth_rate'].grid(column=1, row=0, padx=10, pady=10, rowspan=3)
        
        #Set buttons
        
        # Head Roll Panel
        self.head_roll_frame = tk.LabelFrame(self.master, bd=1, text="Head Roll")
        self.head_roll_frame.grid(column=2, row=0)
        
        # head roll slider
        self.head_roll_pos = tk.DoubleVar()
        self.head_roll_pos.set(self.robot.motors['head_roll'].init_angle)
        self.controls['head_roll_pos'] = tk.Scale(self.head_roll_frame,label="Head Roll", orient=tk.VERTICAL, from_=self.robot.motors['head_roll'].llim_angle,
                                    to=self.robot.motors['head_roll'].ulim_angle, variable=self.head_roll_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.motorPositionSliderCallback, motor='head_roll'))
        self.controls['head_roll_pos'].grid(column=0, row=0, padx=10, pady=10, rowspan=3)
        
        # head roll Rate slider
        self.head_roll_rate = tk.DoubleVar()
        self.head_roll_rate.set(self.robot.motors['head_roll'].rate)
        self.controls['head_roll_rate'] = tk.Scale(self.head_roll_frame,label="Head Roll Rate", orient=tk.VERTICAL, from_=360,
                                    to=0, variable=self.head_roll_rate, length=self.V_SCALE_LEN,
                                    resolution=1, command=partial(self.motorRateSliderCallback, motor='head_roll'))
        self.controls['head_roll_rate'].grid(column=1, row=0, padx=10, pady=10, rowspan=3)
        
        #Set buttons
        
        # Head Yaw Panel
        self.head_yaw_frame = tk.LabelFrame(self.master, bd=1, text="Head Yaw")
        self.head_yaw_frame.grid(column=0, row=1)
        
        # head yaw position slider
        self.head_yaw_pos = tk.DoubleVar()
        self.head_yaw_pos.set(self.robot.motors['head_yaw'].init_angle)
        self.controls['head_yaw_pos'] = tk.Scale(self.head_yaw_frame,label="Head Yaw", orient=tk.HORIZONTAL, from_=self.robot.motors['head_yaw'].llim_angle,
                                    to=self.robot.motors['head_yaw'].ulim_angle, variable=self.head_yaw_pos, length=self.H_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.motorPositionSliderCallback, motor='head_yaw'))
        self.controls['head_yaw_pos'].grid(column=0, row=0, padx=10, pady=10)
        
        # head yaw Rate slider
        self.head_yaw_rate = tk.DoubleVar()
        self.head_yaw_rate.set(self.robot.motors['head_yaw'].rate)
        self.controls['head_yaw_rate'] = tk.Scale(self.head_yaw_frame,label="Head Roll Rate", orient=tk.HORIZONTAL, from_=0,
                                    to=360, variable=self.head_yaw_rate, length=self.H_SCALE_LEN,
                                    resolution=1, command=partial(self.motorRateSliderCallback, motor='head_yaw'))
        self.controls['head_yaw_rate'].grid(column=0, row=1, padx=10, pady=10)
        
        #Set buttons
        
        # Eye Panel
        self.eye_frame = tk.LabelFrame(self.master, bd=1, text="Eyes")
        self.eye_frame.grid(column=1, row=1)
        
        # eye position slider
        self.eye_pos = tk.DoubleVar()
        self.eye_pos.set(self.robot.motors['eyes'].init_angle)
        self.controls['eye_pos'] = tk.Scale(self.eye_frame,label="Eye Position", orient=tk.HORIZONTAL, from_=self.robot.motors['eyes'].llim_angle,
                                    to=self.robot.motors['eyes'].ulim_angle, variable=self.eye_pos, length=self.H_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.motorPositionSliderCallback, motor='eyes'))
        self.controls['eye_pos'].grid(column=0, row=0, padx=10, pady=10)
        
        # eye position Rate slider
        self.eye_rate = tk.DoubleVar()
        self.eye_rate.set(self.robot.motors['eyes'].rate)
        self.controls['eye_rate'] = tk.Scale(self.eye_frame,label="Eye Position Rate", orient=tk.HORIZONTAL, from_=0,
                                    to=360, variable=self.eye_rate, length=self.H_SCALE_LEN,
                                    resolution=1, command=partial(self.motorRateSliderCallback, motor='eyes'))
        self.controls['eye_rate'].grid(column=0, row=1, padx=10, pady=10)
        
        #Set buttons
        
        # Light control
        self.light_panel = tk.LabelFrame(self.master, bd=1, text="Lights", padx=10, pady=10)
        self.light_panel.grid(column=2, row=1)
        
        # Red slider
        self.red_pos = tk.IntVar()
        self.red_pos.set(self.robot.lights['left_eye'].getOut()[0])
        self.controls['red_pos'] = tk.Scale(self.light_panel,label="R", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.red_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.colorCallback)
        self.controls['red_pos'].grid(column=0, row=0, padx=10, pady=10)
        
        # Green slider
        self.green_pos = tk.IntVar()
        self.green_pos.set(self.robot.lights['left_eye'].getOut()[1])
        self.controls['green_pos'] = tk.Scale(self.light_panel,label="G", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.green_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.colorCallback)
        self.controls['green_pos'].grid(column=1, row=0, padx=10, pady=10)
        
        # Blue slider
        self.blue_pos = tk.IntVar()
        self.blue_pos.set(self.robot.lights['left_eye'].getOut()[2])
        self.controls['blue_pos'] = tk.Scale(self.light_panel,label="B", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.blue_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.colorCallback)
        self.controls['blue_pos'].grid(column=2, row=0, padx=10, pady=10)
        
        # fade rate slider
        self.light_fade_rate = tk.DoubleVar()
        self.light_fade_rate.set(self.robot.lights['left_eye'].rate)
        self.controls['light_fade_rate'] = tk.Scale(self.light_panel,label="Fade Rate", orient=tk.VERTICAL, from_=60,
                                    to=0, variable=self.light_fade_rate, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.fadeRateCallback)
        self.controls['light_fade_rate'].grid(column=3, row=0, padx=10, pady=10)
        
        
        # Sound Panel
        self.sound_panel = tk.LabelFrame(self.master, bd=1, text="Soundboard")
        self.sound_panel.grid(column=0, row=2, columnspan=3)
        
        j = 0
        for i in list(self.robot.sounds):
            self.controls[i] = tk.Button(self.sound_panel,text=i, padx=10, pady=10, command=partial(self.soundboardCallback, sound=i))
            self.controls[i].grid(column=j, row=0, padx=10, pady=10)
            j = j + 1
            
        del j
        
        # Script panel
        self.script_panel = tk.LabelFrame(self.master, bd=1, text="Scripts", padx=10, pady=10)
        self.script_panel.grid(column=0, row=3, columnspan=3)
        
        self.controls['Welcome!'] = tk.Button(self.script_panel,text='Welcome!', padx=10, pady=10, command=self.scriptWelcomeCallback)
        self.controls['Welcome!'].grid(column=0, row=0, padx=10, pady=10)
        
    def on_close(self):
        self.robot.deinit()
        self.winfo_toplevel().destroy()
        
if __name__ == '__main__':
    window = cal_panel(janus('calibration.ini', test=True))
    window.mainloop()
    

