import globalV


class Vehicle:
    def __init__(self, timein, x, v, lane, laneid, orig, dest):
        self.timein = timein
        self.timeout = 0
        self.x = 0 # km
        self.globx = 0 #km
        self.v = 0 # km/h
        self.a = 0 # km/h^2
        self.beta = 250 #h^-1
        self.lane = lane
        self.laneid = laneid
        self.leader = None
        self.orig = orig
        self.dest = dest
        self.exited = 0
        self.tempx = 0 #used to update record speed


    def updateV(self):
        self.a = self.beta * (self.lane.u - self.v)
        self.v = self.v + self.a * (globalV.dt / 3600)


    def updateX(self):
        self.tempx = self.x
        if self.leader == None:
            if self.lane.TL == 1:
                self.x = self.x + self.v * (globalV.dt / 3600)
            else:
                self.x = max(min(self.x + self.v * (globalV.dt / 3600), self.lane.length - 0.001), self.x)
        else:
            self.x = max(min(self.x + self.v * (globalV.dt / 3600), self.leader.x - self.lane.jamspacing), self.x)


    def updateglobX(self):
        if self.lane.st == 0:
            self.globx = self.x
        elif self.lane.st == 1:
            self.globx = self.x + self.lane.lastLn.length
        elif self.lane.st == 2:
            self.globx = self.x + self.lane.lastLn.length + self.lane.lastLn.lastLn.length
        elif self.lane.st == 3:
            self.globx = self.x + self.lane.lastLn.length + \
                         self.lane.lastLn.lastLn.length + self.lane.lastLn.lastLn.lastLn.length


    # This is needed because due to signals.  actual speed different than that in updateV()
    def updaterecV(self):
        self.v = (self.x - self.tempx) / (globalV.dt / 3600)