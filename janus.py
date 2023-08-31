import face_motor
import rgb_led_control
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import os, configparser, time, threading, contextlib
from face_motor import *
from rgb_led_control import *
with contextlib.redirect_stdout(None):
    from pygame import mixer

class janus():
    def __init__(self, filename):
        # initialize i2c bus and PCA9685 Module
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c_bus)
        
        # load calibration file
        self.calfile = configparser.ConfigParser()
        self.calfile.read(filename)
        
        self.pwm_period = float(self.calfile['general']['pwm_period'])
        self.update_period = float(self.calfile['general']['update_period'])
        self.pca.frequency = round(1/self.pwm_period)
        
        # create motor dictionary
        self.motors = dict()
        for i in ['eyes', 'eyelids', 'mouth', 'head_roll', 'head_yaw']:
            self.params = self.calfile[i + '.movement']
            self.params.update(self.calfile['motor.' + self.params['type']])
            self.params['pwm_period'] = self.calfile['general']['pwm_period']            
            self.motors[i] = face_motor(self.pca, self.params)
     
        # create light dictionary
        self.LIGHT_MIN = 0
        self.LIGHT_MAX = 0xFFFF
        self.lights = dict()
        for i in ['left_eye', 'right_eye', 'mouth']:
            self.params = self.calfile[i + '.light']
            self.params['pwm_period'] = self.calfile['general']['pwm_period']
            self.lights[i] = rgb_led_control(self.pca, self.params)
            
        # initialize personality mode
        self.GOOD = 0
        self.EVIL = 1
        
        self.personality = self.GOOD        
        
        # create sound dictionary
        mixer.init()
        self.sounds = dict()
        for i in list(self.calfile['sounds']):
            self.sounds[i] = mixer.Sound(os.path.abspath(self.calfile['sounds'][i]))
    
        # initialize output thread
        self.output_thread = threading.Thread(target = self.update_fcn, daemon = True)
        self.output_thread.start()
        
      
    def setPersonality(self, mode):
        self.personality = mode
        if (self.personality == self.EVIL):
            self.motors['head_roll'].setCmd(self.motors['head_roll'].ulim_angle)
            for i in self.lights:
                self.lights[i].setCmd(self.LIGHT_MAX, self.LIGHT_MIN, self.LIGHT_MIN)
        else:
            self.motors['head_roll'].setCmd(self.motors['head_roll'].llim_angle)
            for i in self.lights:
                self.lights[i].setCmd(self.LIGHT_MIN, self.LIGHT_MAX, self.LIGHT_MIN)
    
    def getPersonality(self):
        return self.personality
    
    def setMotorCmd(self, motor, cmd):
        self.motors[motor].setCmd(cmd)
    
    def playSound(self, sound):
        print(sound)
        if sound in self.sounds:
            mixer.stop()
            self.sounds[sound].play()
        
    def update_fcn(self):
        while(True):
            for i in self.motors:
                self.motors[i].update()
                # print(i + ':\tcmd:\t' + str(self.motors[i].getCmd()) + '\tout:\t' + str(self.motors[i].getOutput()) + '\terr:\t' + str(self.motors[i].getErr()))
            for i in self.lights:
                self.lights[i].update()
                
            time.sleep(self.update_period)

if __name__ == '__main__':
    pass
