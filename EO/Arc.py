import basicFunction as basic
import sensitivyParameter as globalV


class arc(object):
    def __init__(self, ID, arcLength, downNode=None):
        self.ID = ID
        self.downstreamNode = downNode
        self.length = arcLength * 1000
        self.capacity = arcLength / (2 * globalV.vehicleEffectiveLength)  # max number of vehicles that can stay
        self.vehicles = []

    def clear(self):
        self.vehicles.clear()

    def timeDepartureArc(self, aimVehicle, timeArrival, timeDeparturePrvious,
                         delayTime):  # time for ith vehicle to leave the arc
        time1 = timeArrival + (self.length / aimVehicle.desiredSpeed)
        time2 = timeDeparturePrvious + (
                aimVehicle.reactionTime + (aimVehicle.effectiveLength / aimVehicle.desiredSpeed))
        res = basic.getMaximum2(time1, time2)
        return res + delayTime

    def timeDepartureArcFirst(self, aimVehicle, timeArrival):  # time for the first vehicle to leave the arc
        return timeArrival + (self.length / aimVehicle.desiredSpeed)

    def getDelay(
            self):  # the delay time for the next vehicle, only dependent on the number of vehicles currently in the arc
        numVehicle = len(self.vehicles)
        currentSpeed = (self.capacity - numVehicle) / self.capacity * globalV.revisedDesiredSpeed  # in km/h
        delayedSpeed = globalV.revisedDesiredSpeed * 0.277778 - currentSpeed
        return self.length / delayedSpeed  # in sec
