import Arc as arc
import Node as node
import random
import VehicleDiscreteFlow as vehicle
import Event as event
import basicFunction as basic
import Arr_Time as arriveTime
from statistics import mean
import sensitivyParameter as parameter
import numpy as np

# initialization of the network
arc4_left = arc.arc("13thTo14th", 0.115)
node3_left = node.nodeIntersection("int13", arc4_left)
node3_left.stopSign = True
arc3_left = arc.arc("12thTo13th", 0.125, node3_left)
node2_left = node.nodeIntersection("int12", arc3_left)
arc2_left = arc.arc("11thTo12th", 0.14, node2_left)
node1_left = node.nodeIntersection("int11", arc2_left)
arc1_left = arc.arc("10thTo11th", 0.165, node1_left)
entranceNode_left = node.nodeIntersection("int10", arc1_left)

arc4_right = arc.arc("13thTo14th", 0.115)
node3_right = node.nodeIntersection("int13", arc4_right)
node3_right.stopSign = True
arc3_right = arc.arc("12thTo13th", 0.125, node3_right)
node2_right = node.nodeIntersection("int12", arc3_right)
arc2_right = arc.arc("11thTo12th", 0.14, node2_right)
node1_right = node.nodeIntersection("int11", arc2_right)
arc1_right = arc.arc("10thTo11th", 0.165, node1_right)
entranceNode_right = node.nodeIntersection("int10", arc1_right)

eventList = []

#f = open("warmUpTable.csv", "w")
#fsens =  open("sensitivity.csv", "a")

def currentAverageSpeed(aimVehicles):
    # this is the calculation of the average speed
    resTime = []
    resSpeed = []
    for i in range(len(aimVehicles)):
        timeSpent = aimVehicles[i].departureTimes['System'] - aimVehicles[i].enterTimes['int10']
        av = (arc1_left.length + arc2_left.length + arc3_left.length) / timeSpent
        resTime.append(timeSpent)
        resSpeed.append(av)
    if len(resTime):
        return [mean(resTime), mean(resSpeed)]
    else:
        return [0, 0]


def putEvent(aimEvent):
    for j in range(len(aimEvent)):
        aimTime = aimEvent[j].triggerTime
        aimVehicle = aimEvent[j].aimVehicle
        aimVehicleID = -1
        if aimVehicle:
            aimVehicleID = aimVehicle.ID
        mark = 0
        for i in range(len(eventList)):
            objVehicleID = -1
            if basic.equal(aimTime, eventList[i].triggerTime):
                if eventList[i].aimVehicle:
                    objVehicleID = eventList[i].aimVehicle.ID
                if aimVehicleID < objVehicleID:
                    eventList.insert(i, aimEvent[j])
                    mark = 1
                    break
            if aimTime < eventList[i].triggerTime:
                eventList.insert(i, aimEvent[j])
                mark = 1
                break
        if mark == 0:
            eventList.append(aimEvent[j])


def singleSim(simTime=arriveTime.globalSimTime):
    arc4_left.clear()
    node3_left.clear()
    node3_left.clear()
    arc3_left.clear()
    node2_left.clear()
    arc2_left.clear()
    node1_left.clear()
    arc1_left.clear()
    entranceNode_left.clear()

    arc4_right.clear()
    node3_right.clear()
    node3_right.clear()
    arc3_right.clear()
    node2_right.clear()
    arc2_right.clear()
    node1_right.clear()
    arc1_right.clear()
    entranceNode_right.clear()
    eventList.clear()

    # put all the vehicles in the system

    vehicleCount = 0
    arriveTime.generate_time(simTime)
    """
    if len(arriveTime.arr_time10) == 0:
        arriveTime.generate_time(simTime)
    if len(arriveTime.arr_time10) == 0:
        print("ERROR! No Car Entering the system")
        return
    """
    vehicles = [[], [], []]
    lastVehicle = [None, None, None]

    for i in range(len(arriveTime.arr_time10)):
        vehicleCount = vehicleCount + 1
        # going left and right
        aimLane = arriveTime.objDirection_10[i]

        if aimLane == 0:
            if len(vehicles[1]) > len(vehicles[2]):
                aimLane = 2
            else:
                aimLane = 1

        if len(vehicles[aimLane]) == 0:
            newVehicle = vehicle.vehicleDiscreteFlow(vehicleCount)
        else:
            newVehicle = vehicle.vehicleDiscreteFlow(vehicleCount, lastVehicle[aimLane])
            lastVehicle[aimLane].follower = newVehicle
        newVehicle.linksToGo = arriveTime.linkToGo_10[i]
        vehicles[aimLane].append(newVehicle)
        vehicles[0].append(newVehicle)
        lastVehicle[aimLane] = newVehicle
        if aimLane == 1:
            newEvent = event.Event_EnterNode(newVehicle, entranceNode_left, arriveTime.arr_time10[i])
        else:
            newEvent = event.Event_EnterNode(newVehicle, entranceNode_right, arriveTime.arr_time10[i])
        eventList.append(newEvent)

    eventRes = []
    # set the traffic light
    # 10: all green
    # 11: 55 green, then 45 red
    # 12: 65 green, then 35 red
    # 14: 50 green, then 50 red

    t = 55
    color = 1  # green
    while t <= simTime:
        eventRes.append(event.Event_NodeTurn(node1_left, t))
        eventRes.append(event.Event_NodeTurn(node1_right, t))
        if color == 1:  # green to red
            t = t + 45
            color = 2
        else:
            t = t + 55
            color = 1

    t = 65
    color = 1  # green
    while t <= simTime:
        eventRes.append(event.Event_NodeTurn(node2_left, t))
        eventRes.append(event.Event_NodeTurn(node2_right, t))
        if color == 1:  # green to red
            t = t + 35
            color = 2
        else:
            t = t + 65
            color = 1

    putEvent(eventRes)
    eventRes.clear()

    vehiclesLeaving = []
    warmUpTable = []
    while len(eventList) > 0:
        if eventList[0].triggerTime > simTime:
            break
        mark = eventList[0].executeEvent()
        if mark:
            eventRes.extend(mark)
            putEvent(eventRes)
        elif eventList[0].aimVehicle is not None:
            if 'System' in eventList[0].aimVehicle.departureTimes:
                vehiclesLeaving.append(eventList[0].aimVehicle)
                #temp = currentAverageSpeed(vehiclesLeaving)
                #warmUpTable.append([eventList[0].triggerTime, temp[0], temp[1]])
        eventList.pop(0)
        eventRes.clear()
    warmUpTime = parameter.warmUpTime

    """
    for i in range(len(warmUpTable)):
        f.write("%d,%lf,%lf,%lf\n" % (
        parameter.warmUpBin * int(warmUpTable[i][0] / parameter.warmUpBin), warmUpTable[i][0],warmUpTable[i][1] , warmUpTable[i][2] * 3.6))
    
    """

    volumeCount = 0
    totalTime = 0
    travelSpeeds = []
    for i in range(len(vehicles[0])):
        if not 'int10' in vehicles[0][i].enterTimes:
            continue
        if not '13thTo14th' in vehicles[0][i].departureTimes:
            continue
        if warmUpTime > vehicles[0][i].enterTimes['int10']:
            # skip the warm up
            continue
        if 'System' in vehicles[0][i].departureTimes:
            volumeCount = volumeCount + 1
            travelTime = vehicles[0][i].departureTimes['System'] - vehicles[0][i].enterTimes['int10']
            travelSpeed = (arc1_left.length + arc2_left.length + arc3_left.length) / travelTime
            travelSpeeds.append(travelSpeed)
            totalTime = totalTime + travelTime

    averageTime = totalTime / volumeCount
    averageSpeed = (arc1_left.length + arc2_left.length + arc3_left.length) / averageTime  # in m/s
    print("The volume is %d, average time is %.2lf, average speed is %.2lf\n" % (
        volumeCount, averageTime, averageSpeed * 3.6))
    volumeCount = volumeCount / (simTime - warmUpTime) * 3600
    return [mean(travelSpeeds), averageTime, volumeCount]


def main(n):
    volume = []
    travelTime = []
    travelSpeeds = []

    #f.write("Interval,Time,TravelTime,Speed\n")
    for i in range(0, n):
        print("Simulating %d Round" % (i + 1))
        res = singleSim()
        travelSpeeds.append(res[0])
        travelTime.append(res[1])
        volume.append(res[2])
    travelTime = basic.mean_confidence_interval(travelTime)
    volume = basic.mean_confidence_interval(volume)
    averageSpeed = basic.mean_confidence_interval(travelSpeeds)
    print(
        "The flow rate is %.1lf+-%.1lf veh/h, average travel time is %.2lf+-%.2lf sec, and average speed is %.2lf+-%.2lf km/h\n" % (
            volume[0], volume[1], travelTime[0], travelTime[1], averageSpeed[0] * 3.6, averageSpeed[1] * 3.6))

    print("The average warm up time is %.1lf sec.\n" % (mean(travelSpeeds)))
    return travelTime[0]
    #f.close()


t = main(100)
#fsens.write("%lf,%lf\n"%(parameter.revisedDesiredSpeed,t))
#fsens.close()