from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO
import os, curses, configparser, time, threading, contextlib, math
from lib.face_motor import *
from lib.rgb_led_control import *
import scripts
with contextlib.redirect_stdout(None):
    from pygame import mixer

class janus():
    def __init__(self, filename, test=False):
        # load calibration file
        self.calfile = configparser.ConfigParser()
        self.calfile.read(filename)
        
        # initialize i2c bus and PCA9685 Modules
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca1 = PCA9685(self.i2c_bus, address=int(self.calfile['pca.1']['addr'], 16))
        self.pwm1_period = float(self.calfile['pca.1']['pwm_period'])
        self.pca1.frequency = round(1/self.pwm1_period)
        if('pca.2' in self.calfile.keys()):
            self.pca2 = PCA9685(self.i2c_bus, address=int(self.calfile['pca.2']['addr'], 16))
            self.pwm2_period = float(self.calfile['pca.2']['pwm_period'])
            self.pca2.frequency = round(1/self.pwm2_period)
        
        self.test_mode = test
        
        # set PWM frequency and update period
        self.update_period = float(self.calfile['general']['update_period'])
        
        
        # create motor dictionary
        self.motors = dict()
        for i in ['eyes', 'eyelids', 'mouth', 'head_roll', 'head_yaw']:
            self.params = self.calfile[i + '.movement']
            self.params.update(self.calfile['motor.' + self.params['type']])
            self.params['pwm_period'] = self.calfile['pca.1']['pwm_period']       
            self.motors[i] = face_motor(self.pca1, self.params)
     
        # create light dictionary
        self.LIGHT_MIN = 0
        self.LIGHT_MAX = 0xFFFF
        self.lights = dict()
        for i in ['eyes', 'mouth']:
            self.params = self.calfile[i + '.lights']
            self.params['update_period'] = self.calfile['general']['update_period']
            if('pca.2' in self.calfile.keys()):
                self.lights[i] = rgb_led_control(self.pca2, self.params)
            else:
                self.lights[i] = rgb_led_control(self.pca1, self.params)

        # set mouth move/blink frequency
        self.talk_frequency = float(self.calfile['general']['mouth_frequency'])
        self.prev_talking = False
        self.mouth_motor_offset = 0.5 * (self.motors['mouth'].ulim_angle - self.motors['mouth'].llim_angle)
            
        # initialize personality mode
        self.GOOD = 0
        self.EVIL = 1
        self.SLEEP = 2
        self.setPersonality(self.SLEEP)
        
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

        # set up remote trigger
        self.REMOTE_CHANNEL = 17
        
        GPIO.setup(self.REMOTE_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.REMOTE_CHANNEL, GPIO.RISING, callback=self.remote_trigger_callback, bouncetime=100)

        
        # initialize output thread
        self.running = True
        self.prev_time = time.time_ns()
        self.output_thread = threading.Thread(target = self.update_fcn, daemon = True)
        self.output_thread.start()
        
      
    def setPersonality(self, mode):

        if (mode == self.EVIL):
            self.setMotorCmd('head_roll', self.motors['head_roll'].ulim_angle)
            self.setMotorCmd('eyelids', self.motors['eyelids'].ulim_angle)
            if (self.personality == self.GOOD):
                self.setMotorCmd('eyes', self.motors['eyes'].ulim_angle - (self.getMotorCmd('eyes') - self.motors['eyes'].llim_angle))

            
            self.lights['eyes'].setCmd(int(self.calfile['color.evil']['eyes_red'], 16),
                                    int(self.calfile['color.evil']['eyes_green'], 16),
                                    int(self.calfile['color.evil']['eyes_blue'], 16))
            self.lights['mouth'].setCmd(int(self.calfile['color.evil']['mouth_red'], 16),
                                    int(self.calfile['color.evil']['mouth_green'], 16),
                                    int(self.calfile['color.evil']['mouth_blue'], 16))
            
        elif (mode == self.GOOD):
            self.setMotorCmd('head_roll', self.motors['head_roll'].llim_angle)
            self.setMotorCmd('eyelids', self.motors['eyelids'].ulim_angle)
            if (self.personality == self.EVIL):
                self.setMotorCmd('eyes', self.motors['eyes'].ulim_angle - (self.getMotorCmd('eyes') - self.motors['eyes'].llim_angle))

            self.lights['eyes'].setCmd(int(self.calfile['color.good']['eyes_red'], 16),
                                    int(self.calfile['color.good']['eyes_green'], 16),
                                    int(self.calfile['color.good']['eyes_blue'], 16))
            self.lights['mouth'].setCmd(int(self.calfile['color.good']['mouth_red'], 16),
                                    int(self.calfile['color.good']['mouth_green'], 16),
                                    int(self.calfile['color.good']['mouth_blue'], 16))
        else:
            self.setMotorCmd('eyes', self.motors['eyes'].init_angle)
            self.setMotorCmd('eyelids', self.motors['eyelids'].llim_angle)
            self.lights['eyes'].setCmd(int(self.calfile['color.sleep']['eyes_red'], 16),
                                    int(self.calfile['color.sleep']['eyes_green'], 16),
                                    int(self.calfile['color.sleep']['eyes_blue'], 16))
            self.lights['mouth'].setCmd(int(self.calfile['color.sleep']['mouth_red'], 16),
                                    int(self.calfile['color.sleep']['mouth_green'], 16),
                                    int(self.calfile['color.sleep']['mouth_blue'], 16))
                
        self.personality = mode
    
    def getPersonality(self):
        return self.personality
    
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
    
    def playSound(self, sound):
        if sound in self.sounds:
            mixer.stop()
            self.sounds[sound].play()
            self.setStatusMsg('Playing: ' + sound)
                
    def isTalking(self):
        return mixer.get_busy()
        
    def setStatusMsg(self, msg):
        self.statusMsg = str(msg)

    def remote_trigger_callback(self, channel):
        if GPIO.input(channel):
            scripts.welcomeScript(self)
        
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
                            self.setCrossfadeRate('mouth', 0)
                        
                        self.setLightCmd('mouth', (self.mouth_light_offset[0] * self.talk_osc) + self.mouth_light_offset[0],
                                         (self.mouth_light_offset[1] * self.talk_osc) + self.mouth_light_offset[1],
                                         (self.mouth_light_offset[2] * self.talk_osc) + self.mouth_light_offset[2])
                                                                        
                    elif (self.getPersonality() == self.EVIL):
                        if not self.prev_talking:
                            self.setMotorRate('mouth', 360)

                        self.setMotorCmd('mouth', (self.mouth_motor_offset * self.talk_osc) + self.mouth_motor_offset)
                        

                    self.prev_talking = True

                else:
                    if self.prev_talking:
                        if (self.getPersonality() == self.GOOD):
                            self.setLightCmd('mouth', self.mouth_amp[0], self.mouth_amp[1], self.mouth_amp[2])                            
                            self.setCrossfadeRate('mouth', float(self.calfile['mouth.lights']['rate']))
                        elif (self.getPersonality() == self.EVIL):
                            self.setMotorRate('mouth', float(self.calfile['mouth.movement']['rate']))
                            self.setMotorCmd('mouth', self.motors['mouth'].init_angle)
                        
                        self.prev_talking = False
                
                
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
        if(self.test_mode):
            curses.nocbreak()
            curses.echo()
            curses.endwin()

if (__name__ == '__main__'):
    pass

