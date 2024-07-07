from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO
import os, curses, configparser, time, threading, contextlib, math
from lib.face_motor import *
from lib.rgb_led_control import *
with contextlib.redirect_stdout(None):
    from pygame import mixer

class mask():
    def __init__(self, filename, test=False):
        # load calibration file
        self.calfile = configparser.ConfigParser()
        self.calfile.read(filename)
        
        # initialize i2c bus and PCA9685 Modules
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca1 = PCA9685(self.i2c_bus, address=int(self.calfile['pca.1']['addr'], 16))
        self.pca1.reset()
        self.pwm1_period = float(self.calfile['pca.1']['pwm_period'])
        self.pca1.frequency = round(1/self.pwm1_period)
        if('pca.2' in self.calfile.keys()):
            self.pca2 = PCA9685(self.i2c_bus, address=int(self.calfile['pca.2']['addr'], 16))
            self.pca2.reset()
            self.pwm2_period = float(self.calfile['pca.2']['pwm_period'])
            self.pca2.frequency = round(1/self.pwm2_period)
        
        self.test_mode = test
        
        # set PWM frequency and update period
        self.update_period = float(self.calfile['general']['update_period'])
        
        
        # create motor dictionary
        self.motors = dict()
        for i in ['tilt', 'pan']:
            self.params = self.calfile['eyes.' + i]
            self.params.update(self.calfile['motor.' + self.params['type']])
            self.params['pwm_period'] = self.calfile['pca.1']['pwm_period']       
            self.motors[i] = face_motor(self.pca1, self.params)
     
        # create light dictionary
        self.LIGHT_MIN = 0
        self.LIGHT_MAX = 0xFFFF
        self.lights = dict()
        for i in ['lights']:
            self.params = self.calfile['eyes.' + i]
            self.params['update_period'] = self.calfile['general']['update_period']
            if('pca.2' in self.calfile.keys()):
                self.lights[i] = rgb_led_control(self.pca2, self.params)
            else:
                self.lights[i] = rgb_led_control(self.pca1, self.params)

        # set up test output screen
        self.statusMsg = ''
        if self.test_mode:
            self.test_out = curses.initscr()
            curses.cbreak()
            curses.noecho()

        # initialize output thread
        self.running = True
        self.prev_time = time.time_ns()
        self.output_thread = threading.Thread(target = self.update_fcn, daemon = True)
        self.output_thread.start()
    
    def setMotorCmd(self, motor, cmd):
        self.motors[motor].setCmd(cmd)

    def getMotorCmd(self, motor):
        return self.motors[motor].getCmd()
        
    def setMotorRate(self, motor, rate):
        self.motors[motor].setRate(rate)
        
    def setLightCmd(self, light, rcmd, gcmd, bcmd):
        self.lights[light].setCmd(rcmd, gcmd, bcmd)

    def getLightCmd(self, light):
        return self.lights[light].getCmd()
            
    def setCrossfadeRate(self, light, rate):
        self.lights[light].setRate(rate)
    
    def isTalking(self):
        return mixer.get_busy()
        
    def setStatusMsg(self, msg):
        self.statusMsg = str(msg)

    def update_fcn(self):
        while(self.running):
            self.c_time = time.time_ns()
            self.e_time = (self.c_time - self.prev_time) * 1e-9
            if (self.e_time >= self.update_period):
                self.prev_time = self.c_time
                
             
                # send motor commands
                for i in self.motors:
                    self.motors[i].update(self.e_time)
                
                # send light commands
                for i in self.lights:
                    self.lights[i].update(self.e_time)
                
                # test mode output
                if(self.test_mode):
                    self.test_out.addstr(0, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}\t{4:>10}'.format(' ','cmd','out','err','rate'))
                    j = 1
                    for i in self.motors:
                        self.test_out.addstr(j, 0, '{0:<10}\t{1:>10.0f}\t{2:>10.0f}\t{3:>10.0f}\t{4:>10}'.format(i,self.motors[i].getCmd(),self.motors[i].getOutput(),self.motors[i].getErr(),self.motors[i].getRate()))
                        j = j + 1
                    
                    j = j + 1    
                    for i in self.lights:
                        self.test_out.addstr(j, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}\t{4:>10}'.format(i + ' red',self.lights[i].getCmd()[0],self.lights[i].getOut()[0],self.lights[i].getErr()[0],self.lights[i].getRate()))
                        j = j + 1   
                        self.test_out.addstr(j, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}\t{4:>10}'.format(i + ' green',self.lights[i].getCmd()[1],self.lights[i].getOut()[1],self.lights[i].getErr()[1],self.lights[i].getRate()))
                        j = j + 1   
                        self.test_out.addstr(j, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}\t{4:>10}'.format(i + ' blue',self.lights[i].getCmd()[2],self.lights[i].getOut()[2],self.lights[i].getErr()[2],self.lights[i].getRate()))     
                        j = j + 1
                        
                    self.test_out.addstr(j, 0, 'Interval: {:0.2f} seconds'.format(self.e_time))
                    j = j + 1
                    self.test_out.addstr(j, 0, '{:<80}'.format(self.statusMsg))
                    self.test_out.refresh()
                
    def deinit(self):
        self.running = False
        self.output_thread.join()
        self.pca1.deinit()
        if('pca.2' in self.calfile.keys()):
            self.pca2.deinit()
        if(self.test_mode):
            curses.nocbreak()
            curses.echo()
            curses.endwin()

if (__name__ == '__main__'):
    pass

