import VehicleDiscreteFlow as vehicle
import basicFunction as basic


def timeEnterNode(aimVehicle, timeArrival, timeEnterPrevious):  # the time of ith vehicle to enter the arc
    return basic.getMaximum2(timeArrival,
                            timeEnterPrevious + aimVehicle.reactionTime + (aimVehicle.effectiveLength / aimVehicle.desiredSpeed))

def timeEnterArcFirst(timeArrival): # this is only for the first vehicle
    return timeArrival

class nodeIntersection(object):
    def __init__(self, ID, downArc = None):
        self.ID = ID
        self.downstreamArc = downArc
        self.vehicles = []
        self.trafficSignal = True # true for green, false for red
        self.stopSign = False

    def clear(self):
        self.vehicles.clear()
