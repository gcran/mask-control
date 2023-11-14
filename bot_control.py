#!./.venv/bin/python
import tkinter as tk
from lib.janus import janus
from functools import partial
import contextlib
with contextlib.redirect_stdout(None):
    from pygame import mixer

# import scripts
import scripts

class bot_control(tk.Frame):
    def __init__(self, robot, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("J4N-U5 Control Panel")
        self.SCALE_RES = 0.1
        self.H_SCALE_LEN = 500
        self.V_SCALE_LEN = 200
        
        self.robot = robot
        self.winfo_toplevel().protocol('WM_DELETE_WINDOW', self.on_close)
        
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

        self.updateWidgets()
        
        for i in self.controls:
            self.controls[i]['state'] = tk.NORMAL

    def updateWidgets(self):
        self.eyelid_pos.set(self.robot.getMotorCmd('eyelids'))
        self.mouth_pos.set(self.robot.getMotorCmd('mouth'))
        self.head_yaw_pos.set(self.robot.getMotorCmd('head_yaw'))
        self.eye_pos.set(self.robot.getMotorCmd('eyes'))
        
    def createWidgets(self):
        self.controls = dict()
        # head yaw position slider
        self.head_yaw_pos = tk.DoubleVar()
        self.head_yaw_pos.set(self.robot.motors['head_yaw'].init_angle)
        self.controls['head_yaw_pos'] = tk.Scale(self.master,label="Head Yaw", orient=tk.HORIZONTAL, from_=self.robot.motors['head_yaw'].llim_angle,
                                    to=self.robot.motors['head_yaw'].ulim_angle, variable=self.head_yaw_pos, length=self.H_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.headYawSliderCallback)
        self.controls['head_yaw_pos'].grid(column=2, row=0, padx=10, pady=10, columnspan=3)
        
        # eye position slider
        self.eye_pos = tk.DoubleVar()
        self.eye_pos.set(self.robot.motors['eyes'].init_angle)
        self.controls['eye_pos'] = tk.Scale(self.master,label="Eye Position", orient=tk.HORIZONTAL, from_=self.robot.motors['eyes'].llim_angle,
                                    to=self.robot.motors['eyes'].ulim_angle, variable=self.eye_pos, length=self.H_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.eyeSliderCallback)
        self.controls['eye_pos'].grid(column=2, row=1, padx=10, pady=10, columnspan=3)
        
        # eyelid position slider
        self.eyelid_pos = tk.DoubleVar()
        self.eyelid_pos.set(self.robot.motors['eyelids'].init_angle)
        self.controls['eyelid_pos'] = tk.Scale(self.master,label="Eyelids", orient=tk.VERTICAL, from_=self.robot.motors['eyelids'].llim_angle,
                                    to=self.robot.motors['eyelids'].ulim_angle, variable=self.eyelid_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.eyelidSliderCallback)
        self.controls['eyelid_pos'].grid(column=0, row=0, padx=10, pady=10, rowspan=2)
        
        # mouth position slider
        self.mouth_pos = tk.DoubleVar()
        self.mouth_pos.set(self.robot.motors['mouth'].init_angle)
        self.controls['mouth_pos'] = tk.Scale(self.master,label="Mouth", orient=tk.VERTICAL, from_=self.robot.motors['mouth'].llim_angle,
                                    to=self.robot.motors['mouth'].ulim_angle, variable=self.mouth_pos, length=self.V_SCALE_LEN,
                                    resolution=self.SCALE_RES, command=self.mouthSliderCallback)
        self.controls['mouth_pos'].grid(column=1, row=0, padx=10, pady=10, rowspan=2)
        
        # personality selector
        self.personalityFrame = tk.LabelFrame(self.master, bd=1, text="Personality", padx=10, pady=10)
        self.personalityFrame.grid(column=6, row=0)
        self.personality = tk.IntVar()
        self.controls['radio_security'] = tk.Radiobutton(self.personalityFrame, text="Security",value=self.robot.SECURITY,
                                                variable=self.personality, command=self.personalityCallback)
        self.controls['radio_friendly'] = tk.Radiobutton(self.personalityFrame, text="Good",value=self.robot.FRIENDLY,
                                                variable=self.personality, command=self.personalityCallback)
        self.controls['radio_sleep'] = tk.Radiobutton(self.personalityFrame, text="Sleep",value=self.robot.SLEEP,
                                                variable=self.personality, command=self.personalityCallback)
        
        self.controls['radio_sleep'].grid(column=0,row=0, sticky=tk.W)
        self.controls['radio_security'].grid(column=0,row=1, sticky=tk.W)
        self.controls['radio_friendly'].grid(column=0,row=2, sticky=tk.W)
        self.controls['radio_sleep'].select()
        self.controls['radio_security'].deselect()
        self.controls['radio_friendly'].deselect()
        
        self.SoundboardFrame = tk.LabelFrame(self.master, bd=1, text="Soundboard")
        self.SoundboardFrame.grid(column=0, row=2, columnspan=3)
        
        j = 0
        for i in list(self.robot.sounds):
            self.controls[i] = tk.Button(self.SoundboardFrame,text=i, padx=10, pady=10, command=partial(self.soundboardCallback, sound=i))
            self.controls[i].grid(column=j, row=0, padx=10, pady=10)
            j = j + 1
            
        del j
        # Script panel
        self.script_panel = tk.LabelFrame(self.master, bd=1, text="Scripts", padx=10, pady=10)
        self.script_panel.grid(column=0, row=3, columnspan=3)
        
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
    window = bot_control(janus('calibration.ini', test=False))
    window.mainloop()

