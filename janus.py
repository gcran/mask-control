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
        
        # load calibration file
        self.calfile = configparser.ConfigParser()
        self.calfile.read(filename)
        
        self.freq = int(self.calfile['general']['frequency'], 10)
        self.update_rate = int(self.calfile['general']['update_period'])
        self.pca.frequency = self.freq
        
        #initialize devices
        self.maxcount = 0xfff
        
        self.minpulse = float(self.calfile['eye.movement']['minpulse'])
        self.maxpulse = float(self.calfile['eye.movement']['maxpulse'])
        self.eye_move_llimcount = round(self.maxcount * (self.minpulse / (1/self.freq))) * 0x10
        self.eye_move_ulimcount = round(self.maxcount * (self.maxpulse / (1/self.freq))) * 0x10
        self.eye_move_maxstep = float(self.calfile['eye.movement']['maxstep'])
        self.slope_eye_move = (self.eye_move_ulimcount - self.eye_move_llimcount) / float(self.calfile['eye.movement']['range'])
        self.eye_move_uangle = float(self.calfile['eye.movement']['uangle'])
        self.eye_move_langle = float(self.calfile['eye.movement']['langle'])
        self.eye_move = face_motor(self.pca, int(self.calfile['eye.movement']['channel'], 10), \
                                    self.eye_move_llimcount, \
                                    self.eye_move_ulimcount)
        
        
        self.minpulse = float(self.calfile['eyelid.movement']['minpulse'])
        self.maxpulse = float(self.calfile['eyelid.movement']['maxpulse'])
        self.eyelid_move_llimcount = round(self.maxcount * (self.minpulse / (1/self.freq))) * 0x10
        self.eyelid_move_ulimcount = round(self.maxcount * (self.maxpulse / (1/self.freq))) * 0x10        
        self.eyelid_move_maxstep = float(self.calfile['eyelid.movement']['maxstep'])
        self.slope_eyelid_move = (self.eyelid_move_ulimcount - self.eyelid_move_llimcount) / float(self.calfile['eyelid.movement']['range'])
        self.eyelid_move_uangle = float(self.calfile['eyelid.movement']['uangle'])
        self.eyelid_move_langle = float(self.calfile['eyelid.movement']['langle'])
        self.eyelid = face_motor(self.pca, int(self.calfile['eyelid.movement']['channel'], 10), \
                                    self.eyelid_move_llimcount, \
                                    self.eyelid_move_ulimcount)
        
        self.minpulse = float(self.calfile['mouth.movement']['minpulse'])
        self.maxpulse = float(self.calfile['mouth.movement']['maxpulse'])
        self.mouth_move_llimcount = round(self.maxcount * (self.minpulse / (1/self.freq))) * 0x10
        self.mouth_move_ulimcount = round(self.maxcount * (self.maxpulse / (1/self.freq))) * 0x10        
        self.mouth_move_maxstep = float(self.calfile['mouth.movement']['maxstep'])
        self.slope_mouth_move = (self.mouth_move_ulimcount - self.mouth_move_llimcount) / float(self.calfile['mouth.movement']['range'])
        self.mouth_move_uangle = float(self.calfile['mouth.movement']['uangle'])
        self.mouth_move_langle = float(self.calfile['mouth.movement']['langle'])
        self.mouth = face_motor(self.pca, int(self.calfile['mouth.movement']['channel'], 10), \
                                    self.mouth_move_llimcount, \
                                    self.mouth_move_ulimcount)
        
        self.minpulse = float(self.calfile['head_yaw.movement']['minpulse'])
        self.maxpulse = float(self.calfile['head_yaw.movement']['maxpulse'])
        self.head_yaw_move_llimcount = round(self.maxcount * (self.minpulse / (1/self.freq))) * 0x10
        self.head_yaw_move_ulimcount = round(self.maxcount * (self.maxpulse / (1/self.freq))) * 0x10        
        self.head_yaw_move_maxstep = float(self.calfile['head_yaw.movement']['maxstep'])
        self.slope_head_yaw_move = (self.head_yaw_move_ulimcount - self.head_yaw_move_llimcount) / float(self.calfile['head_yaw.movement']['range'])
        self.head_yaw_move_uangle = float(self.calfile['head_yaw.movement']['uangle'])
        self.head_yaw_move_langle = float(self.calfile['head_yaw.movement']['langle'])
        self.head_yaw = face_motor(self.pca, int(self.calfile['head_yaw.movement']['channel'], 10), \
                                    self.head_yaw_move_llimcount, \
                                    self.head_yaw_move_ulimcount)
                                    
        self.minpulse = float(self.calfile['head_roll.movement']['minpulse'])
        self.maxpulse = float(self.calfile['head_roll.movement']['maxpulse'])
        self.head_roll_move_llimcount = round(self.maxcount * (self.minpulse / (1/self.freq))) * 0x10
        self.head_roll_move_ulimcount = round(self.maxcount * (self.maxpulse / (1/self.freq))) * 0x10        
        self.head_roll_move_maxstep = float(self.calfile['head_roll.movement']['maxstep'])
        self.slope_head_roll_move = (self.head_roll_move_ulimcount - self.head_roll_move_llimcount) / float(self.calfile['head_roll.movement']['range'])
        self.head_roll_move_uangle = float(self.calfile['head_roll.movement']['uangle'])
        self.head_roll_move_langle = float(self.calfile['head_roll.movement']['langle'])
        self.head_roll = face_motor(self.pca, int(self.calfile['head_roll.movement']['channel'], 10), \
                                    self.head_roll_move_llimcount, \
                                    self.head_roll_move_ulimcount)
        
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
        self.mouth_color_g_cmd = 0xffff
        self.mouth_color_b_cmd = 0x0
        
        self.eye_pos_out_count = 0x0
        self.eyelid_pos_out_count = 0x0
        self.mouth_pos_out_count = 0x0
        self.head_yaw_pos_out_count = 0x0        
        self.head_roll_pos_out_count = 0x0
        
        self.eye_pos_cmd_angle = 0x0
        self.eyelid_pos_cmd_angle = 0x0
        self.mouth_pos_cmd_angle = 0x0
        self.head_yaw_pos_cmd_angle = 0x0
        self.head_roll_pos_cmd_angle = 0x0
        
    def setEyeColor(self, r_cmd, g_cmd, b_cmd):
        self.eye_color_r_cmd = r_cmd
        self.eye_color_g_cmd = g_cmd
        self.eye_color_b_cmd = b_cmd
        
    def setMouthColor(self, r_cmd, g_cmd, b_cmd):
        self.mouth_color_r_cmd = r_cmd
        self.mouth_color_g_cmd = g_cmd
        self.mouth_color_b_cmd = b_cmd
        
    def setEyePositionCmd(self, cmd):
        self.eye_pos_cmd_angle = max(self.eye_move_langle, min(self.eye_move_uangle, cmd))
        
    def setEyeLidPositionCmd(self, cmd):
        self.eyelid_pos_cmd_angle = max(self.eyelid_move_langle, min(self.eyelid_move_uangle, cmd))
        
    def setMouthPositionCmd(self, cmd):
        self.mouth_pos_cmd_angle = cmd
        
    def setHeadYawPositionCmd(self, cmd):
        self.head_yaw_pos_cmd_angle = cmd
        
    def setHeadRollPositionCmd(self, cmd):
        self.head_roll_pos_cmd_angle = cmd
        
    def update(self):
        self.eye_pos_cmd_count = round((self.eye_pos_cmd_angle * self.slope_eye_move) + self.eye_move_llimcount)
        self.eye_pos_err = self.eye_pos_cmd_count - self.eye_pos_out_count
        self.eye_pos_step = max(-self.eye_move_maxstep, min(self.eye_move_maxstep, self.eye_pos_err))
        self.eye_pos_out_count = self.eye_pos_out_count + self.eye_pos_step
        self.eye_move.setCmd(self.eye_pos_out_count)
                
        self.eyelid_pos_cmd_count = round((self.eyelid_pos_cmd_angle * self.slope_eyelid_move) + self.eyelid_move_llimcount)
        self.eyelid_pos_err = self.eyelid_pos_cmd_count - self.eyelid_pos_out_count
        self.eyelid_pos_step = max(-self.eyelid_move_maxstep, min(self.eyelid_move_maxstep, self.eyelid_pos_err))
        self.eyelid_pos_out_count = self.eyelid_pos_out_count + self.eyelid_pos_step
        self.eyelid.setCmd(self.eyelid_pos_out_count)
                
        self.mouth_pos_cmd_count = round((self.mouth_pos_cmd_angle * self.slope_mouth_move) + self.mouth_move_llimcount)
        self.mouth_pos_err = self.mouth_pos_cmd_count - self.mouth_pos_out_count
        self.mouth_pos_step = max(-self.mouth_move_maxstep, min(self.mouth_move_maxstep, self.mouth_pos_err))
        self.mouth_pos_out_count = self.mouth_pos_out_count + self.mouth_pos_step
        self.mouth.setCmd(self.mouth_pos_out_count)
        
        self.head_yaw_pos_cmd_count = round((self.head_yaw_pos_cmd_angle * self.slope_head_yaw_move) + self.head_yaw_move_llimcount)
        self.head_yaw_pos_err = self.head_yaw_pos_cmd_count - self.head_yaw_pos_out_count
        self.head_yaw_pos_step = max(-self.head_yaw_move_maxstep, min(self.head_yaw_move_maxstep, self.head_yaw_pos_err))
        self.head_yaw_pos_out_count = self.head_yaw_pos_out_count + self.head_yaw_pos_step
        self.head_yaw.setCmd(self.head_yaw_pos_out_count)
        # print(str(self.head_yaw_pos_cmd_count) + " " + str(self.head_yaw_pos_out_count) + " " + str(self.head_yaw_pos_err))
        
        self.head_roll_pos_cmd_count = round((self.head_roll_pos_cmd_angle * self.slope_head_roll_move) + self.head_roll_move_llimcount)
        self.head_roll_pos_err = self.head_roll_pos_cmd_count - self.head_roll_pos_out_count
        self.head_roll_pos_step = max(-self.head_roll_move_maxstep, min(self.head_roll_move_maxstep, self.head_roll_pos_err))
        self.head_roll_pos_out_count = self.head_roll_pos_out_count + self.head_roll_pos_step
        self.head_roll.setCmd(self.head_roll_pos_out_count)
                
        self.eye_light.setCmd(self.eye_color_r_cmd, self.eye_color_g_cmd, self.eye_color_b_cmd)
        # print(str(self.eye_color_r_cmd) + " " + str(self.eye_color_g_cmd) + " " + str(self.eye_color_b_cmd))
        self.mouth_light.setCmd(self.mouth_color_r_cmd, self.mouth_color_g_cmd, self.mouth_color_b_cmd)
        
    def getRate(self):
        return self.update_rate
        
        
