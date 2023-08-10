class rgvb_led_control():
	def __init__(self, pca, rchannel, gchannel, bchannel):
		self.pca = pca
		self.rchannel = rchannel
		self.gchannel = gchannel
		self.bchannel = bchannel
		self.llim = 0x0
		self.ulim = 0xFFFF
		self.maxstep = 0x0700
		self.routput = 0xFFFF
		self.goutput = 0xFFFF
		self.boutput = 0xFFFF
		
	def setCmd(self, rcmd, gcmd, bcmd):
		self.rerr = rcmd - self.routput
		self.gerr = gcmd - self.goutput
		self.berr = bcmd - self.boutput
		
		self.rstep = max(-self.maxstep, min(self.maxstep, self.rerr))
		self.gstep = max(-self.maxstep, min(self.maxstep, self.gerr))
		self.bstep = max(-self.maxstep, min(self.maxstep, self.berr))
		
		self.routput = max(self.llim, min(self.ulim, self.routput + self.rstep))
		self.goutput = max(self.llim, min(self.ulim, self.goutput + self.gstep))
		self.boutput = max(self.llim, min(self.ulim, self.boutput + self.bstep))
		
		self.pca.channels[self.rchannel].duty_cycle = self.routput
		self.pca.channels[self.gchannel].duty_cycle = self.goutput
		self.pca.channels[self.bchannel].duty_cycle = self.boutput
		
		# print(str(self.routput) + " " + str(self.goutput) + " " + str(self.boutput))
