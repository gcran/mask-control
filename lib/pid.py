import time


class pid:
    def __init__(self, kP=1, kI=0, kD=0):
        # initialize gains
        self.kP = kP
        self.kI = kI
        self.kD = kD

    def init_cond(self):
        self.currTime = time.time()
        self.prevTime = self.currTime
        self.prevErr = 0
        self.cP = 0
        self.cI = 0
        self.cD = 0

    def update(self, err):

        self.currTime = time.time()
        self.prevTime = self.currTime
        deltaTime = self.currTime - self.prevTime
        deltaError = err - self.prevError

        self.cP = self.kP * err

        self.cI = deltaTime * self.kI * err

        self.cD = self.kI * (deltaError / deltaTime) if deltaTime > 0 else 0

        self.prevTime self.currTime
        self.prevErr = err
        return sum([self.cP, self.cI, self.cD])
