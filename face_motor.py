class face_motor():
	"""Class for a servo in the robot face.
	   Set ulim, lli, and slew from calibration file.
	   Assumes a speed of 60 degrees/150 ms."""
	def __init__(self, pca, channel, llim, ulim, step):
		self.pca = pca
		self.channel = channel
		self.ulim = min(ulim, 0x0FFFF)
		self.llim = max(llim, 0)
		self.speed = 400
		self.scalefactor = (self.ulim - self.llim) / (0xFFFF)
		self.maxstep = step
		self.output = round(self.scalefactor * ((self.ulim + self.llim) / 2) + self.llim)
		
	def setCmd(self, cmd):
		self.poscmd = round(self.scalefactor * cmd + self.llim)
		self.err = self.poscmd - self.output
		self.step = max(-self.maxstep, min(self.maxstep, self.err))
		self.output = max(self.llim, min(self.output + self.step, self.ulim))			
		self.pca.channels[self.channel].duty_cycle = self.output
		
		# print(str(self.poscmd) + " " + str(self.output) + " " + str(self.err))
		
	def getPos(self):
		return self.output	

