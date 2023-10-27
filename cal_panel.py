#!/usr/bin/python
import tkinter as tk
from lib.janus import janus
from functools import partial
import contextlib

from scripts import eyes_center
with contextlib.redirect_stdout(None):
    from pygame import mixer

# import scripts
import scripts

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
        self.robot.setMotorRate(motor, int(cmd))
        
    def eyesColorCallback(self, cmd):
        self.robot.setLightCmd('eyes', self.eyes_red_pos.get(),self.eyes_green_pos.get(),self.eyes_blue_pos.get())
        
    def mouthColorCallback(self, cmd):
        self.robot.setLightCmd('mouth', self.mouth_red_pos.get(),self.mouth_green_pos.get(),self.mouth_blue_pos.get())
    
    def fadeRateCallback(self, cmd, light):
        self.robot.setCrossfadeRate(light, float(cmd))
    
    def soundboardCallback(self, sound):
        self.robot.playSound(sound)

    def personalityCallback(self):
        self.robot.setPersonality(self.personality.get())
        self.updateWidgets()
        
    def scriptCallback(self, script):
        for i in self.controls:
            self.controls[i]['state'] = tk.DISABLED
            
        if script == 'blink':
            scripts.blink(self.robot)
        
        if script == 'eyes_center':
            scripts.eyes_center(self.robot)

        if script == 'eyes_closed':
            scripts.eyes_closed(self.robot)

        if script == 'eyes_half_open':
            scripts.eyes_half_open(self.robot)
            
        if script == 'eyes_open':
            scripts.eyes_open(self.robot)

        if script == 'eyes_left':
            scripts.eyes_left(self.robot)

        if script == 'eyes_right':
            scripts.eyes_right(self.robot)

        if script == 'head_center':
            scripts.head_center(self.robot)

        if script == 'head_left':
            scripts.head_left(self.robot)

        if script == 'head_right':
            scripts.head_right(self.robot)

        if script == 'head_tilt_45':
            scripts.head_tilt_45(self.robot)

        if script == 'head_straight':
            scripts.head_straight(self.robot)

        if script == 'scan':
            scripts.scan(self.robot)            

        if script == 'welcome':
            scripts.welcomeScript(self.robot)

        if script == 'scan':
            scripts.scan(self.robot)            

        if script == 'lights_off':
            scripts.lights_off(self.robot)            

        if script == 'lights_red':
            scripts.lights_red(self.robot)    

        if script == 'lights_green':
            scripts.lights_green(self.robot)    

        if script == 'lights_blue':
            scripts.lights_blue(self.robot)    

        if script == 'lights_white':
            scripts.lights_white(self.robot)           

        if script == 'security_mode':
            scripts.security_mode(self.robot)

        if script == 'security_mod_infinite':
            scripts.security_mode_infinite(self.robot)      



        self.updateWidgets()
        
        for i in self.controls:
            self.controls[i]['state'] = tk.NORMAL
        
    def updateWidgets(self):
        self.eyelid_pos.set(self.robot.getMotorCmd('eyelids'))
        self.mouth_pos.set(self.robot.getMotorCmd('mouth'))
        self.head_roll_pos.set(self.robot.getMotorCmd('head_roll'))
        self.head_yaw_pos.set(self.robot.getMotorCmd('head_yaw'))
        self.eye_pos.set(self.robot.getMotorCmd('eyes'))

        self.eyes_red_pos.set(self.robot.getLightCmd('eyes')[0])
        self.eyes_green_pos.set(self.robot.getLightCmd('eyes')[1])
        self.eyes_blue_pos.set(self.robot.getLightCmd('eyes')[2])

        self.mouth_red_pos.set(self.robot.getLightCmd('mouth')[0])
        self.mouth_green_pos.set(self.robot.getLightCmd('mouth')[1])
        self.mouth_blue_pos.set(self.robot.getLightCmd('mouth')[2])
    
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
        
        # personality selector
        self.personalityFrame = tk.LabelFrame(self.master, bd=1, text="Personality", padx=10, pady=10)
        self.personalityFrame.grid(column=3, row=0)
        self.personality = tk.IntVar()
        self.controls['radio_good'] = tk.Radiobutton(self.personalityFrame, text="Good",value=self.robot.GOOD,
                                                variable=self.personality, command=self.personalityCallback)
        self.controls['radio_evil'] = tk.Radiobutton(self.personalityFrame, text="Evil",value=self.robot.EVIL,
                                                variable=self.personality, command=self.personalityCallback)
        self.controls['radio_sleep'] = tk.Radiobutton(self.personalityFrame, text="Sleep",value=self.robot.SLEEP,
                                                variable=self.personality, command=self.personalityCallback)
        
        self.controls['radio_sleep'].grid(column=0,row=0, sticky=tk.W)
        self.controls['radio_good'].grid(column=0,row=1, sticky=tk.W)
        self.controls['radio_evil'].grid(column=0,row=2, sticky=tk.W)
        self.controls['radio_sleep'].select()
        self.controls['radio_good'].deselect()
        self.controls['radio_evil'].deselect()
        
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

        # Mouth Light control
        self.light_panel = tk.LabelFrame(self.master, bd=1, text="Mouth Lights", padx=10, pady=10)
        self.light_panel.grid(column=3, row=1)
        
        # Red slider
        self.mouth_red_pos = tk.IntVar()
        self.mouth_red_pos.set(self.robot.lights['mouth'].getOut()[0])
        self.controls['mouth_red_pos'] = tk.Scale(self.light_panel,label="R", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.mouth_red_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.mouthColorCallback)
        self.controls['mouth_red_pos'].grid(column=0, row=0, padx=10, pady=10)
        
        # Green slider
        self.mouth_green_pos = tk.IntVar()
        self.mouth_green_pos.set(self.robot.lights['mouth'].getOut()[1])
        self.controls['mouth_green_pos'] = tk.Scale(self.light_panel,label="G", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.mouth_green_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.mouthColorCallback)
        self.controls['mouth_green_pos'].grid(column=1, row=0, padx=10, pady=10)
        
        # Blue slider
        self.mouth_blue_pos = tk.IntVar()
        self.mouth_blue_pos.set(self.robot.lights['mouth'].getOut()[2])
        self.controls['mouth_blue_pos'] = tk.Scale(self.light_panel,label="B", orient=tk.VERTICAL, from_=65535,
                                    to=0, variable=self.mouth_blue_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.mouthColorCallback)
        self.controls['mouth_blue_pos'].grid(column=2, row=0, padx=10, pady=10)
        
        # fade rate slider
        self.mouth_light_fade_rate = tk.DoubleVar()
        self.mouth_light_fade_rate.set(self.robot.lights['mouth'].rate)
        self.controls['mouth_light_fade_rate'] = tk.Scale(self.light_panel,label="Fade Rate", orient=tk.VERTICAL, from_=10,
                                    to=0, variable=self.mouth_light_fade_rate, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=partial(self.fadeRateCallback, light = 'mouth'))
        self.controls['mouth_light_fade_rate'].grid(column=3, row=0, padx=10, pady=10)
        
        
        # Sound Panel
        self.sound_panel = tk.LabelFrame(self.master, bd=1, text="Soundboard")
        self.sound_panel.grid(column=0, row=2, columnspan=4)
        
        j = 0
        for i in list(self.robot.sounds):
            self.controls[i] = tk.Button(self.sound_panel,text=i, padx=10, pady=10, command=partial(self.soundboardCallback, sound=i))
            self.controls[i].grid(column=j, row=0, padx=10, pady=10)
            j = j + 1
            
        del j
        
        # Script panel
        self.script_panel = tk.LabelFrame(self.master, bd=1, text="Scripts", padx=10, pady=10)
        self.script_panel.grid(column=0, row=3, columnspan=4)
        
        self.controls['welcome'] = tk.Button(self.script_panel,text='Welcome!', padx=10, pady=10, command=partial(self.scriptCallback, script='welcome'))
        self.controls['welcome'].grid(column=0, row=0, padx=10, pady=10)        
        self.controls['blink'] = tk.Button(self.script_panel,text='Blink', padx=10, pady=10, command=partial(self.scriptCallback, script='blink'))
        self.controls['blink'].grid(column=1, row=0, padx=10, pady=10)        
        self.controls['eyes closed'] = tk.Button(self.script_panel,text='Eyes Closed', padx=10, pady=10, command=partial(self.scriptCallback, script='eyes_closed'))
        self.controls['eyes closed'].grid(column=2, row=0, padx=10, pady=10)
        self.controls['eyes half open'] = tk.Button(self.script_panel,text='Eyes Half Open', padx=10, pady=10, command=partial(self.scriptCallback, script='eyes_half_open'))
        self.controls['eyes half open'].grid(column=3, row=0, padx=10, pady=10)
        self.controls['eyes open'] = tk.Button(self.script_panel,text='Eyes Open', padx=10, pady=10, command=partial(self.scriptCallback, script='eyes_open'))
        self.controls['eyes open'].grid(column=4, row=0, padx=10, pady=10)
        self.controls['eyes left'] = tk.Button(self.script_panel,text='Eyes Left', padx=10, pady=10, command=partial(self.scriptCallback, script='eyes_left'))
        self.controls['eyes left'].grid(column=5, row=0, padx=10, pady=10)
        self.controls['eyes center'] = tk.Button(self.script_panel,text='Eyes Center', padx=10, pady=10, command=partial(self.scriptCallback, script='eyes_center'))
        self.controls['eyes center'].grid(column=6, row=0, padx=10, pady=10)
        self.controls['eyes right'] = tk.Button(self.script_panel,text='Eyes Right', padx=10, pady=10, command=partial(self.scriptCallback, script='eyes_right'))
        self.controls['eyes right'].grid(column=7, row=0, padx=10, pady=10)
        self.controls['head left'] = tk.Button(self.script_panel,text='Head Left', padx=10, pady=10, command=partial(self.scriptCallback, script='head_left'))
        self.controls['head left'].grid(column=0, row=1, padx=10, pady=10)
        self.controls['head center'] = tk.Button(self.script_panel,text='Head Center', padx=10, pady=10, command=partial(self.scriptCallback, script='head_center'))
        self.controls['head center'].grid(column=1, row=1, padx=10, pady=10)
        self.controls['head right'] = tk.Button(self.script_panel,text='Head Right', padx=10, pady=10, command=partial(self.scriptCallback, script='head_right'))
        self.controls['head right'].grid(column=2, row=1, padx=10, pady=10)
        self.controls['head tilt 45'] = tk.Button(self.script_panel,text='Head Tilt 45', padx=10, pady=10, command=partial(self.scriptCallback, script='head_tilt_45'))
        self.controls['head tilt 45'].grid(column=3, row=1, padx=10, pady=10)
        self.controls['head straight'] = tk.Button(self.script_panel,text='Head Straight', padx=10, pady=10, command=partial(self.scriptCallback, script='head_straight'))
        self.controls['head straight'].grid(column=4, row=1, padx=10, pady=10)
        self.controls['scan'] = tk.Button(self.script_panel,text='Scan', padx=10, pady=10, command=partial(self.scriptCallback, script='scan'))
        self.controls['scan'].grid(column=5, row=1, padx=10, pady=10)
        self.controls['security mode'] = tk.Button(self.script_panel,text='Security Mode', padx=10, pady=10, command=partial(self.scriptCallback, script='security_mode'))
        self.controls['security mode'].grid(column=6, row=1, padx=10, pady=10)
        self.controls['security mode_infinite'] = tk.Button(self.script_panel,text='Security Mode Infinite', padx=10, pady=10, command=partial(self.scriptCallback, script='security_mode_infinite'))
        self.controls['security mode_infinite'].grid(column=6, row=1, padx=10, pady=10)
        self.controls['lights off'] = tk.Button(self.script_panel,text='Lights Off', padx=10, pady=10, command=partial(self.scriptCallback, script='lights_off'))
        self.controls['lights off'].grid(column=0, row=2, padx=10, pady=10)
        self.controls['lights red'] = tk.Button(self.script_panel,text='Lights red', padx=10, pady=10, command=partial(self.scriptCallback, script='lights_red'))
        self.controls['lights red'].grid(column=1, row=2, padx=10, pady=10)
        self.controls['lights green'] = tk.Button(self.script_panel,text='Lights green', padx=10, pady=10, command=partial(self.scriptCallback, script='lights_green'))
        self.controls['lights green'].grid(column=2, row=2, padx=10, pady=10)
        self.controls['lights blue'] = tk.Button(self.script_panel,text='Lights blue', padx=10, pady=10, command=partial(self.scriptCallback, script='lights_blue'))
        self.controls['lights blue'].grid(column=3, row=2, padx=10, pady=10)
        self.controls['lights white'] = tk.Button(self.script_panel,text='Lights white', padx=10, pady=10, command=partial(self.scriptCallback, script='lights_white'))
        self.controls['lights white'].grid(column=4, row=2, padx=10, pady=10)
        
    def on_close(self):
        self.robot.deinit()
        self.winfo_toplevel().destroy()
        
if __name__ == '__main__':
    window = cal_panel(janus('calibration.ini', test=True))
    window.mainloop()
    

