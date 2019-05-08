from Lane import Lane
import globalV # global variables
import numpy as np
import Arr_Time as arrtime
import statistics
import math
# import matplotlib.pyplot as plt


finaltt = []
finalvel = []
finalvol = []


while globalV.simnumber <= globalV.totalsim:
    globalV.all_vehs = []
    #Simulate one-direction two-lane traffic from 10th to 14th on Peachtree
    # Initialize Road Network
    # 13rd to 14th
    ln4 = Lane(0.115, None, 3)
    # 12nd to 13rd
    ln3 = Lane(0.125, ln4, 2)
    # 11st to 12nd
    ln2 = Lane(0.14, ln3, 1)
    # 10th to 11st
    ln1 = Lane(0.165, ln2, 0)

    ln1.lastLn = None
    ln2.lastLn = ln1
    ln3.lastLn = ln2
    ln4.lastLn = ln3

    all_ln = [ln1, ln2, ln3, ln4]


    # Generate B-type event list (Vehicle entry at each street) done in Arr_Time.py
    # Assumption: vehicle inter-arrival time follows log-normal distribution
    # arrival time is a list, which consists the arrival time of vehicles.
    arr = arrtime.generate_time()
    dest = arrtime.linkToGo_10     # number of links that the car will go before leaving the system
    turn = arrtime.objDirection_10
    signals = globalV.generate_signaltime()


    # identify warm-up
    # ttt1 = []
    # ttt2 = []
    # travel = []
    # vel = []



    # Run Simulation
    for t in np.arange(0, globalV.sim_time, globalV.dt):
        # Event: update signal
        for tempLn in all_ln:
            if len(signals[tempLn.st]) > 0 and t > signals[tempLn.st][0]:
                tempLn.update_signal()
                signals[tempLn.st].pop(0)

        # update all vehicles' speed and location on each lane
        for tempLn in all_ln:
            for templnVeh in tempLn.cars:
                for tempVeh in templnVeh:
                    tempVeh.updateV()
                    tempVeh.updateX()
                    tempVeh.updateglobX()
                    tempVeh.updaterecV()  # due to signals.  actual speed different than that in updateV()

        # C-type event
        # to see if the vehicles enter the next road segment
        for tempLn in all_ln:
            tempLn.veh_transfer(t)

        # scan B-type event
        # Event: vehicle entry at each street at given times
        for tempLn in all_ln:
            if len(arr[tempLn.st]) > 0 and t > arr[tempLn.st][0]:
                if tempLn.st == 0:
                    tempdest = dest[0]
                    tempturn = turn[0]
                else:
                    tempdest = 4
                    tempturn = 0
                if tempLn.st == 0 and tempLn.cars:
                    tempLn.veh_arrival(t, tempdest, tempturn)
                    if tempLn.arrflag == 1:
                        arr[tempLn.st].pop(0)
                        dest.pop(0)
                        turn.pop(0)
                else:
                    # only when side street is green (Peachtree is red TL == 0, let vehicles in)
                    if tempLn.lastLn.TL == 0 or tempLn.st == 3:
                        tempLn.veh_arrival(t, tempdest, tempturn)
                        if tempLn.arrflag == 1:
                            arr[tempLn.st].pop(0)


        # Warm-up period
        # identify warm-up using travel time
        # if round(t * 5) % 30 == 0:
        #     TT = []
        #     for tempVeh in AS.globalV.all_vehs:
        #         if tempVeh.timeout != 0 and tempVeh.orig == 0 and tempVeh.dest == 4:
        #             traveltime = tempVeh.timeout - tempVeh.timein
        #             TT.append(traveltime)
        #     if len(TT) > 0:
        #         ttt1.append(t)
        #         travel.append(statistics.mean(TT))

        # identify warm-up using speed
        # if round(t * 5) % 30 == 0:
        #     Vel = []
        #     for tempVeh in AS.globalV.all_vehs:
        #         if tempVeh.exited == 0:
        #             speed = tempVeh.v
        #             Vel.append(speed)
        #     if len(Vel) > 0:
        #         ttt2.append(t)
        #         vel.append(statistics.mean(Vel))
        #
        # Verification

        # verification 1
        # plot current vehicles
        # if round(t * 5) % 1500 == 0:
        #     X = []
        #     Y = []
        #     for tempVeh in globalV.all_vehs:
        #         if tempVeh.exited == 0:
        #             x = tempVeh.globx
        #             y = tempVeh.laneid
        #             X.append(x)
        #             Y.append(y)
        #     plt.xlabel('x / km')
        #     plt.ylabel('y / lane')
        #     plt.scatter(X,Y)
        #     plt.show()


        # verification 2
        # print vehicle positions
        # if t > 1000 and t < 1003:
        #     for tempVeh in AS.globalV.all_vehs:
        #         if tempVeh.exited == 0:
        #             print('position', tempVeh.globx * 1000, 'time', t)



    # identify warm-up
    # plt.plot(ttt1, travel, label = 'Travel Time')
    # plt.plot(ttt2, vel, 'y', label = 'Average Speed')
    # plt.xlabel('t / second')
    # plt.show()


    # Output
    TT = []
    Vel = []

    volumn = 0
    for tempVeh in globalV.all_vehs:
        if tempVeh.timeout != 0 and tempVeh.timeout > 250 and tempVeh.orig == 0 and tempVeh.dest == 4:
            traveltime = tempVeh.timeout - tempVeh.timein
            speed = (ln1.length + ln2.length + ln3.length + ln4.length) / (traveltime / 3600)
            volumn += 1
            TT.append(traveltime)
            Vel.append(speed)
    # print(statistics.mean(TT))
    # print(statistics.mean(Vel))
    # print(simnumber)
    # print(TT)


    volumn = volumn * 3600 / (1800 - 250)
    finaltt.append(statistics.mean(TT))
    finalvel.append(statistics.mean(Vel))
    finalvol.append(volumn)
    print('average travel time in', globalV.simnumber, 'th simulation', statistics.mean(TT))
    print('average speed in', globalV.simnumber, 'th simulation', statistics.mean(Vel))
    print('flow rate in', globalV.simnumber, 'th simulation', volumn)
    globalV.simnumber += 1


widtt = 1.96 * statistics.stdev(finaltt) / math.sqrt(globalV.totalsim)
widvel = 1.96 * statistics.stdev(finalvel) / math.sqrt(globalV.totalsim)
widvol = 1.96 * statistics.stdev(finalvol) / math.sqrt(globalV.totalsim)
print('CI of average travel time', statistics.mean(finaltt), '+-', widtt, 'seconds')
print('CI of average speed', statistics.mean(finalvel), '+-', widvel, 'km / hr')
print('CI of flow rate', statistics.mean(finalvol), '+-', widvol, 'vehicles / hr')
