import random
from Vehicle import Vehicle
import globalV


class Lane:
    def __init__(self, length, nextLn, st):
        self.u = globalV.desiredSpeed # km/hr
        self.jamden = 150.0 #veh/km
        self.jamspacing = 1.0 / self.jamden #km
        self.cars = [[], []]
        self.pos = 0
        self.length = length
        self.lastLn = None
        self.nextLn = nextLn
        self.TL = 1 # 1 for green 0 for red
        self.st = st # 0 for 10 to 11, 1 for 11 to 12, 2 for 12 to 13, 3 for 13 to 14
        self.arrflag = 0  # 1 means vehicle succeffully generated


    def veh_arrival(self, time, dest, turn):
        self.arrflag = 1
        # turn: 0 straight, 1 left turn, 2 right turn
        if turn == 0:
            temp = random.randint(0, 1)
        elif turn == 1:
            temp = 1
        else:
            temp = 0
        if len(self.cars[temp]) == 0 or (len(self.cars[temp]) > 0  and self.cars[temp][-1].x > self.jamspacing):
            tempVeh = Vehicle(time, 0, 31, self, temp, self.st, dest)
            if len(self.cars[temp]) > 0:
                tempVeh.leader = self.cars[temp][-1]
            else:
                tempVeh.leader = None
            self.cars[temp].append(tempVeh)
            globalV.all_vehs.append(tempVeh)
        else:
            self.arrflag = 0


    def veh_transfer(self, time):
        for templnVeh in self.cars:
            if len(templnVeh) > 0:
                tempVeh = templnVeh[0]
                if tempVeh.x > self.length and tempVeh.lane.TL == 1:
                    # transfer or remove or stay
                    exitflag = 1
                    # transfer or stay
                    if self.nextLn != None and self.nextLn.st != tempVeh.dest:
                        exitflag = 0
                        # transfer
                        if len(self.nextLn.cars[tempVeh.laneid]) == 0 \
                                or self.nextLn.cars[tempVeh.laneid][-1].x > self.jamspacing:
                            tempVeh.x -= self.length
                            tempVeh.lane = self.nextLn
                            if len(self.nextLn.cars[tempVeh.laneid]) > 0:
                                tempVeh.leader = self.nextLn.cars[tempVeh.laneid][-1]
                            else:
                                tempVeh.leader = None
                            self.nextLn.cars[tempVeh.laneid].append(tempVeh)
                        # stay
                        else:
                            pass

                    # remove from last link
                    if exitflag == 1:
                        tempVeh.exited = 1
                        tempVeh.timeout = time
                    templnVeh.pop(0)
                    if len(templnVeh) > 0:
                        templnVeh[0].leader = None


    def update_signal(self):
        self.TL = 1 - self.TL




