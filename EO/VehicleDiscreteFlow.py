import basicFunction as basic
import sensitivyParameter as parameter

class vehicleDiscreteFlow(object):
    def __init__(self, ID, leader = None, length=parameter.vehicleEffectiveLength, reactionTime=parameter.reactionTime,
                 desiredSpeed=parameter.revisedDesiredSpeed):
        self.effectiveLength = length
        self.reactionTime = basic.randomNormalVariable(reactionTime,
                                              0.05)  # a small random variable for generating reaction time
        self.desiredSpeed = desiredSpeed * 0.277778
        self.enterTimes = dict()
        self.departureTimes = dict()
        self.leader = leader
        self.follower = None
        self.ID = ID
        self.isFirstCar = False
        self.linksToGo = 4
        self.totalTraveledDistance = 0