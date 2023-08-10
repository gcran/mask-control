import face_motor
import rgb_led_control
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import configparser
from face_motor import *
from eye_color_control import *

class janus():
    def __init__(self, filename):
        # initialize i2c bus and PCA9685 Module
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c_bus)
        self.pca.frequency = 50
        # load calibration file
        self.calfile = configparser.ConfigParser()
        self.calfile.read(filename)
        
        self.update_rate = int(self.calfile['general']['update_period'])
        #initialize devices
        self.eye_move = face_motor(self.pca, int(self.calfile['eye.movement']['channel'], 10), \
                                    int(self.calfile['eye.movement']['llim'], 16), \
                                    int(self.calfile['eye.movement']['ulim'],  16), \
                                    int(self.calfile['eye.movement']['maxstep'],  16))
        
        self.eye_lid = face_motor(self.pca, int(self.calfile['eyelid.movement']['channel'], 10), \
                                    int(self.calfile['eyelid.movement']['llim'], 16), \
                                    int(self.calfile['eyelid.movement']['ulim'],  16), \
                                    int(self.calfile['eyelid.movement']['maxstep'],  16))
        
        self.mouth_move = face_motor(self.pca, int(self.calfile['mouth.movement']['channel'], 10), \
                                    int(self.calfile['mouth.movement']['llim'], 16), \
                                    int(self.calfile['mouth.movement']['ulim'],  16), \
                                    int(self.calfile['mouth.movement']['maxstep'],  16))
        
        self.head_pivot = face_motor(self.pca, int(self.calfile['head.pivot']['channel'], 10), \
                                    int(self.calfile['head.pivot']['llim'], 16), \
                                    int(self.calfile['head.pivot']['ulim'],  16), \
                                    int(self.calfile['head.pivot']['maxstep'],  16))
        
        self.eye_light = rgb_led_control(self.pca, int(self.calfile['eye.light']['rchannel'], 10), \
                                            int(self.calfile['eye.light']['gchannel'], 10), \
                                            int(self.calfile['eye.light']['bchannel'], 10))
        
        self.mouth_light = rgb_led_control(self.pca, int(self.calfile['mouth.light']['rchannel'], 10), \
                                                int(self.calfile['mouth.light']['gchannel'], 10), \
                                                int(self.calfile['mouth.light']['bchannel'], 10))
        
        # initialize setpoints
        self.eye_color_r_cmd = 0x0
        self.eye_color_g_cmd = 0x0
        self.eye_color_b_cmd = 0x0
        
        self.mouth_color_r_cmd = 0x0
        self.mouth_color_g_cmd = 0x0
        self.mouth_color_b_cmd = 0x0
        
        self.eye_pos_cmd = 0x0
        self.eyelid_pos_cmd = 0x0
        self.mouth_pos_cmd = 0x0
        self.head_pos_cmd = 0x0
        
    def setEyeColor(self, r_cmd, g_cmd, b_cmd):
        self.eye_color_r_cmd = r_cmd
        self.eye_color_g_cmd = g_cmd
        self.eye_color_b_cmd = b_cmd
        
    def setMouthColor(self, r_cmd, g_cmd, b_cmd):
        self.mouth_color_r_cmd = r_cmd
        self.mouth_color_g_cmd = g_cmd
        self.mouth_color_b_cmd = b_cmd
        
    def setEyePosition(self, cmd):
        self.eye_pos_cmd = cmd
        
    def setEyeLidPosition(self, cmd):
        self.eyelid_pos_cmd = cmd
        
    def setMouthPosition(self, cmd):
        self.mouth_pos_cmd = cmd
        
    def setHeadPosition(self, cmd):
        self.head_pos_cmd = cmd
        
    def update(self):
        self.eye_move.setCmd(self.eye_pos_cmd)
        self.eye_lid.setCmd(self.eyelid_pos_cmd)
        self.mouth_move.setCmd(self.mouth_pos_cmd)
        self.head_pivot.setCmd(self.head_pos_cmd)
        
        self.eye_light.setCmd(self.eye_color_r_cmd, self.eye_color_g_cmd, self.eye_color_b_cmd)
        self.mouth_light.setCmd(self.mouth_color_r_cmd, self.mouth_color_g_cmd, self.mouth_color_b_cmd)
        
    def getRate(self):
        return self.update_rate
        
        
