class face_motor():
	"""Class for a servo in the robot face.
	   Set ulim, lli, and slew from calibration file.
	   Assumes a speed of 60 degrees/150 ms."""
	def __init__(self, pca, channel, llim, ulim):
		self.pca = pca
		self.channel = channel
		self.ulim = min(ulim, 0x0FFFF)
		self.llim = max(llim, 0)
		self.output = round((self.ulim + self.llim) / 2)
		self.pca.channels[self.channel].duty_cycle = self.output
		# print(str(self.llim) + " " + str(self.ulim))
		
	def setCmd(self, cmd):
		# self.err = cmd - self.output
		# self.step = max(-self.maxstep, min(self.maxstep, self.err))
		self.output = round(max(self.llim, min(self.ulim, cmd)))
		self.pca.channels[self.channel].duty_cycle = self.output
		
		# print(str(cmd))
		
	def getPos(self):
		return self.output	

