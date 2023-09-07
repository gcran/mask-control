from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import os, curses, configparser, time, threading, contextlib, math
from lib.face_motor import *
from lib.rgb_led_control import *
with contextlib.redirect_stdout(None):
    from pygame import mixer

class janus():
    def __init__(self, filename, test=False):
        # load calibration file
        self.calfile = configparser.ConfigParser()
        self.calfile.read(filename)
        
        # initialize i2c bus and PCA9685 Module
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca1 = PCA9685(self.i2c_bus, address=int(self.calfile['pca1']['addr'], 16))
        
        self.test_mode = test
        
        # set PWM frequency and update period
        self.pwm_period = float(self.calfile['general']['pwm_period'])
        self.update_period = float(self.calfile['general']['update_period'])
        self.pca1.frequency = round(1/self.pwm_period)
        
        # create motor dictionary
        self.motors = dict()
        for i in ['eyes', 'eyelids', 'mouth', 'head_roll', 'head_yaw']:
            self.params = self.calfile[i + '.movement']
            self.params.update(self.calfile['motor.' + self.params['type']])
            self.params['pwm_period'] = self.calfile['general']['pwm_period']            
            self.motors[i] = face_motor(self.pca1, self.params)
     
        # create light dictionary
        self.LIGHT_MIN = 0
        self.LIGHT_MAX = 0xFFFF
        self.lights = dict()
        for i in ['eyes', 'mouth']:
            self.params = self.calfile[i + '.lights']
            self.params['update_period'] = self.calfile['general']['update_period']
            self.lights[i] = rgb_led_control(self.pca1, self.params)

        # set mouth move/blink frequency
        self.talk_frequency = 8
        self.prev_talking = False
        self.mouth_motor_offset = 0.5 * (self.motors['mouth'].ulim_angle - self.motors['mouth'].llim_angle)
            
        # initialize personality mode
        self.GOOD = 0
        self.EVIL = 1
        self.setPersonality(self.GOOD)
        
        # create sound dictionary
        mixer.init()
        self.sounds = dict()
        for i in list(self.calfile['sounds']):
            self.sounds[i] = mixer.Sound(os.path.abspath(self.calfile['sounds'][i]))
            
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
        
    def setmotorRate(self, motor, rate):
        self.motors[motor].setRate(rate)
        
    def setLightCmd(self, light, rcmd, gcmd, bcmd):
        self.lights[light].setCmd(rcmd, gcmd, bcmd)
            
    def setCrossfadeRate(self, light, rate):
        self.lights[light].setRate(rate)
    
    def playSound(self, sound):
        if sound in self.sounds:
            mixer.stop()
            self.sounds[sound].play()
            self.setStatusMsg('Playing: ' + sound)
                
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
                
                # if a sound is playing, flap the mouth/blink the mouth lights, depending on personality
                if self.isTalking():
                    
                    self.talk_osc = math.sin(time.time() * math.tau * self.talk_frequency)
                    if (self.getPersonality() == self.GOOD):
                        if not self.prev_talking:
                            self.mouth_amp = self.lights['mouth'].getOut()
                            self.mouth_light_offset = (self.mouth_amp[0] * 0.5, self.mouth_amp[1] * 0.5, self.mouth_amp[2] * 0.5)
                            self.setCrossfadeRate('mouth', 0xFFFF)
                        
                        self.setLightCmd('mouth', (self.mouth_light_offset[0] * self.talk_osc) + self.mouth_light_offset[0],
                                         (self.mouth_light_offset[1] * self.talk_osc) + self.mouth_light_offset[1],
                                         (self.mouth_light_offset[2] * self.talk_osc) + self.mouth_light_offset[2])
                        
                    elif (self.getPersonality() == self.EVIL):
                        if not self.prev_talking:
                            self.setmotorRate('mouth', 360)

                        self.setMotorCmd('mouth', (self.mouth_motor_offset * self.talk_osc) + self.mouth_motor_offset)

                    self.prev_talking = True

                else:
                    if self.prev_talking:
                        self.setLightCmd('mouth', self.mouth_amp[0], self.mouth_amp[1], self.mouth_amp[2])
                        self.setCrossfadeRate('mouth', float(self.calfile['mouth.lights']['rate']))
                        self.setmotorRate('mouth', float(self.calfile['mouth.movement']['rate']))
                        self.prev_talking = False
                
                # send motor commands
                for i in self.motors:
                    self.motors[i].update(self.e_time)
                
                # send light commands
                for i in self.lights:
                    self.lights[i].update(self.e_time)
                
                # test mode output
                if(self.test_mode):
                    self.test_out.addstr(0, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}'.format(' ','cmd','out','err'))
                    j = 1
                    for i in self.motors:
                        self.test_out.addstr(j, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}'.format(i,self.motors[i].getCmd(),self.motors[i].getOutput(),self.motors[i].getErr()))
                        j = j + 1
                        
                    self.test_out.addstr(j, 0, '\n{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}'.format(' ','R','G','B'))
                    j = j + 2
                    for i in self.lights:
                        self.test_out.addstr(j, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}'.format(i,self.lights[i].getOut()[0],self.lights[i].getOut()[1],self.lights[i].getOut()[2]))     
                        j = j + 1
                        
                    self.test_out.addstr(j, 0, 'Interval: {:0.2f} seconds'.format(self.e_time))
                    j = j + 1
                    self.test_out.addstr(j, 0, '{:<80}'.format(self.statusMsg))
                    self.test_out.refresh()
                
    def deinit(self):
        self.running = False
        self.output_thread.join()
        if(self.test_mode):
            curses.nocbreak()
            curses.echo()
            curses.endwin()

if (__name__ == '__main__'):
    pass

