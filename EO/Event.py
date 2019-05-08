import VehicleDiscreteFlow as vehicle
import Arc as arc
import Node as node
import sensitivyParameter as parameter

class EOEvent(object):
    def __init__(self):
        self.triggerTime = -1
        self.aimVehicle = None

    def executeEvent(self):
        raise NotImplementedError


class Event_ExitSystem(EOEvent):
    def __init__(self, aimVehicle, aimTime):
        EOEvent.__init__(self)
        self.aimVehicle = aimVehicle
        self.triggerTime = aimTime


    def executeEvent(self):
        self.aimVehicle.departureTimes['System'] = self.triggerTime
        if self.aimVehicle.leader is not None:
            self.aimVehicle.leader.follower = self.aimVehicle.follower
        if self.aimVehicle.follower is not None:
            self.aimVehicle.follower.leader = self.aimVehicle.leader
        return False


class Event_EnterNode(EOEvent):  # the next event is enter of an arc
    def __init__(self, aimVehicle, aimNode, aimTime):
        EOEvent.__init__(self)
        self.aimVehicle = aimVehicle
        self.aimNode = aimNode
        self.triggerTime = aimTime
        self.aimVehicle.enterTimes[self.aimNode.ID] = self.triggerTime

    def executeEvent(self):
        #print("Vehilce %d is Entering Node %s at Time %.2lf\n"%(self.aimVehicle.ID,self.aimNode.ID,self.triggerTime) )
        if self.aimNode.trafficSignal:
            if self.aimVehicle.leader is not None:
                aimTime = node.timeEnterNode(self.aimVehicle, self.triggerTime,
                                             self.aimVehicle.leader.enterTimes[self.aimNode.downstreamArc.ID])
            else:
                aimTime = node.timeEnterArcFirst(self.triggerTime)
            if self.aimNode.stopSign:
                aimTime = aimTime + parameter.stopSignDelay
            res = []
            newEvent = Event_EnterArc(self.aimVehicle, self.aimNode.downstreamArc, aimTime)
            res.append(newEvent)
            return res
        else:
            self.aimNode.vehicles.append(self.aimVehicle)
            return False


class Event_NodeTurn(EOEvent):
    def __init__(self, aimNode, aimTime):
        EOEvent.__init__(self)
        self.aimNode = aimNode
        self.triggerTime = aimTime

    def executeEvent(self):
        #print(
            #"Node %s is Turning at Time %.2lf" % (self.aimNode.ID, self.triggerTime))
        if self.aimNode.trafficSignal: # from Green to Red
            #print(" Red\n")
            self.aimNode.trafficSignal = False
            return False
        else: # from Red to Green
            #print(" Green\n")
            self.aimNode.trafficSignal = True
            res = []
            while len(self.aimNode.vehicles):
                if len(res)>0:
                    aimTime = node.timeEnterNode(self.aimNode.vehicles[0], self.triggerTime,
                                                 self.aimNode.vehicles[0].leader.enterTimes[self.aimNode.downstreamArc.ID])
                else:
                    aimTime = node.timeEnterArcFirst(self.triggerTime)
                newEvent = Event_EnterArc(self.aimNode.vehicles[0], self.aimNode.downstreamArc, aimTime)
                res.append(newEvent)
                self.aimNode.vehicles.pop(0)
            return res


class Event_EnterArc(EOEvent):  # the next event is the departure of an arc
    def __init__(self, aimVehicle, aimArc, aimTime):
        EOEvent.__init__(self)
        self.aimVehicle = aimVehicle
        self.aimArc = aimArc
        self.triggerTime = aimTime
        self.aimVehicle.enterTimes[self.aimArc.ID] = self.triggerTime

    def executeEvent(self):
        #print("Vehilce %d is Entering Arc %s at Time %.2lf\n"%(self.aimVehicle.ID,self.aimArc.ID,self.triggerTime) )
        if len(self.aimArc.vehicles) > 0:
            delayTime = self.aimArc.getDelay()
            aimTime = self.aimArc.timeDepartureArc(self.aimVehicle, self.triggerTime,
+                                                   self.aimVehicle.leader.enterTimes[self.aimArc.ID], delayTime)
        else:
            aimTime = self.aimArc.timeDepartureArcFirst(self.aimVehicle, self.triggerTime)
        self.aimArc.vehicles.append(self.aimVehicle)
        res = []
        newEvent = Event_DepartureArc(self.aimVehicle,self.aimArc,aimTime)
        res.append(newEvent)
        return res


class Event_DepartureArc(EOEvent):
    def __init__(self, aimVehicle, aimArc, aimTime):
        EOEvent.__init__(self)
        self.aimVehicle = aimVehicle
        self.aimArc = aimArc
        self.triggerTime = aimTime
        self.aimVehicle.departureTimes[self.aimArc.ID] = self.triggerTime

    def executeEvent(self):
        #print("Vehilce %d is Departuring Arc %s at Time %.2lf\n"%(self.aimVehicle.ID,self.aimArc.ID,self.triggerTime) )
        if len(self.aimArc.vehicles) > 0:
            self.aimArc.vehicles.pop(0)
        else:
            print("ERROR!")
        res = []
        self.aimVehicle.linksToGo -= 1
        self.aimVehicle.totalTraveledDistance += self.aimArc.length
        if self.aimVehicle.linksToGo ==0:
            newEvent = Event_ExitSystem(self.aimVehicle, self.triggerTime)
        elif self.aimArc.downstreamNode is not None:
            newEvent = Event_EnterNode(self.aimVehicle, self.aimArc.downstreamNode, self.triggerTime)
        else:
            newEvent = Event_ExitSystem(self.aimVehicle, self.triggerTime)

        res.append(newEvent)
        return res
