#!./.venv/bin/python
import tkinter as tk
from lib.mask import janus
from functools import partial
import contextlib

with contextlib.redirect_stdout(None):
    from pygame import mixer

class cal_panel(tk.Frame):
    def __init__(self, robot, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Mask Calibration Panel")
        self.SCALE_RES = 0.1
        self.H_SCALE_LEN = 200
        self.V_SCALE_LEN = 200
        
        self.winfo_toplevel().protocol('WM_DELETE_WINDOW', self.on_close)
        self.robot = robot
        
        self.createWidgets()
                
    def motorPositionSliderCallback(self, cmd, motor):
        self.robot.setMotorCmd(motor, float(cmd))
        
    def motorRateSliderCallback(self, cmd, motor):
        self.robot.setMotorRate(motor, int(cmd))
        
    def eyesColorCallback(self, cmd):
        self.robot.setLightCmd('eyes', self.eyes_red_pos.get(),self.eyes_green_pos.get(),self.eyes_blue_pos.get())
        
    def fadeRateCallback(self, cmd, light):
        self.robot.setCrossfadeRate(light, float(cmd))
    
  
    def updateWidgets(self):
        self.tilt_pos.set(self.robot.getMotorCmd('tilt'))
        self.pan_pos.set(self.robot.getMotorCmd('pan'))

        self.eyes_red_pos.set(self.robot.getLightCmd('eyes')[0])
        self.eyes_green_pos.set(self.robot.getLightCmd('eyes')[1])
        self.eyes_blue_pos.set(self.robot.getLightCmd('eyes')[2])
    
    def createWidgets(self):
        
        self.controls = dict()
        # Motor Panel
        self.motor_frame = tk.LabelFrame(self.master, bd=1, text="Motors")
        self.motor_frame.grid(column=0, row=0)
        
        # Tilt Motor Slider
        self.tilt_pos = tk.DoubleVar()
        self.tilt_pos.set(self.robot.motors['tilt'].init_angle)
        self.controls['tilt_pos'] = tk.Scale(self.motor_frame,label="Tilt Position", orient=tk.VERTICAL, from_=self.robot.motors['tilt'].llim_angle,
                                    to=self.robot.motors['tilt'].ulim_angle, variable=self.tilt_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.motorPositionSliderCallback, motor='tilt'))
        self.controls['tilt_pos'].grid(column=0, row=0, padx=10, pady=10, rowspan=3)
        
        # Tilt Motor Rate Slider
        self.tilt_rate = tk.DoubleVar()
        self.tilt_rate.set(self.robot.motors['tilt'].rate)
        self.controls['tilt_rate'] = tk.Scale(self.motor_frame,label="Tilt Rate", orient=tk.VERTICAL, from_=360,
                                    to=0, variable=self.tilt_rate, length=self.V_SCALE_LEN,
                                    resolution=1, command=partial(self.motorRateSliderCallback, motor='tilt'))
        self.controls['tilt_rate'].grid(column=1, row=0, padx=10, pady=10, rowspan=3)
        
        # Pan Motor Slider
        self.pan_pos = tk.DoubleVar()
        self.pan_pos.set(self.robot.motors['pan'].init_angle)
        self.controls['pan_pos'] = tk.Scale(self.pan_frame,label="Pan Position", orient=tk.VERTICAL, from_=self.robot.motors['pan'].llim_angle,
                                    to=self.robot.motors['pan'].ulim_angle, variable=self.pan_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.motorPositionSliderCallback, motor='pan'))
        self.controls['pan_pos'].grid(column=2, row=0, padx=10, pady=10, rowspan=3)
        
        # Pan Motor Rate Slider
        self.pan_rate = tk.DoubleVar()
        self.pan_rate.set(self.robot.motors['pan'].rate)
        self.controls['pan_rate'] = tk.Scale(self.pan_frame,label="Pan Rate", orient=tk.VERTICAL, from_=360,
                                    to=0, variable=self.pan_rate, length=self.V_SCALE_LEN,
                                    resolution=1, command=partial(self.motorRateSliderCallback, motor='pan'))
        self.controls['pan_rate'].grid(column=3, row=0, padx=10, pady=10, rowspan=3)
        
       
        # Eye Light control
        self.light_panel = tk.LabelFrame(self.master, bd=1, text="Eye Lights", padx=10, pady=10)
        self.light_panel.grid(column=2, row=1)
        
        # Red slider
        self.eyes_red_pos = tk.IntVar()
        self.eyes_red_pos.set(self.robot.lights['eyes'].getOut()[0])
        self.controls['eyes_red_pos'] = tk.Scale(self.light_panel,label="R", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.eyes_red_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.eyesColorCallback)
        self.controls['eyes_red_pos'].grid(column=0, row=0, padx=10, pady=10)
        
        # Green slider
        self.eyes_green_pos = tk.IntVar()
        self.eyes_green_pos.set(self.robot.lights['eyes'].getOut()[1])
        self.controls['eyes_green_pos'] = tk.Scale(self.light_panel,label="G", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.eyes_green_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.eyesColorCallback)
        self.controls['eyes_green_pos'].grid(column=1, row=0, padx=10, pady=10)
        
        # Blue slider
        self.eyes_blue_pos = tk.IntVar()
        self.eyes_blue_pos.set(self.robot.lights['eyes'].getOut()[2])
        self.controls['eyes_blue_pos'] = tk.Scale(self.light_panel,label="B", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.eyes_blue_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.eyesColorCallback)
        self.controls['eyes_blue_pos'].grid(column=2, row=0, padx=10, pady=10)
        
        # fade rate slider
        self.eyes_light_fade_rate = tk.DoubleVar()
        self.eyes_light_fade_rate.set(self.robot.lights['eyes'].rate)
        self.controls['eye_light_fade_rate'] = tk.Scale(self.light_panel,label="Fade Rate", orient=tk.VERTICAL, from_=10,
                                    to=0, variable=self.eyes_light_fade_rate, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.fadeRateCallback, light = 'eyes'))
        self.controls['eye_light_fade_rate'].grid(column=3, row=0, padx=10, pady=10)

         
    def on_close(self):
        self.robot.deinit()
        self.winfo_toplevel().destroy()
        
if __name__ == '__main__':
    window = cal_panel(janus('calibration.ini', test=True))
    window.mainloop()
    

