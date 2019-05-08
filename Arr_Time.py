import random
import numpy
import time

arr_time10 = []
linkToGo_10 = [] # number of l2inks that the car will go before leaving the system
objDirection_10 = [] #0 straight, 1 left turn, 2 right turn
arr_time11 = []
arr_time12 = []
arr_time13 = []
globalSimTime = 1800

def generate_time(Sim_time = globalSimTime):


    lgm10 = 1.18642284
    lgs10 = 1.07569549
    lgm11 = 5.6638771
    lgs11 = 0.2979011
    lgm12 = 3.7199815
    lgs12 = 1.9696008
    lgm13 = 3.661255
    lgs13 = 1.1952896

    arr_time10.clear()
    linkToGo_10.clear()  # number of l2inks that the car will go before leaving the system
    objDirection_10.clear()  # 0 straight, 1 left turn, 2 right turn
    arr_time11.clear()
    arr_time12.clear()
    arr_time13.clear()

    #randomSeed = 1 # please change it when we are actually using this one
    randomSeed = int(round(time.time() * 1000)) % 4294967296
    #print(randomSeed)
    numpy.random.seed(randomSeed)
    ### Arrival time from 10 st
    t = 0
    while t < Sim_time:
        t += numpy.random.lognormal(lgm10, lgs10)
        whereToGo = numpy.random.random()
        if t < Sim_time:
            arr_time10.append(t)
            if whereToGo < 0.02:
                linkToGo_10.append(1)
                objDirection_10.append(2)
            elif whereToGo < 0.04:
                linkToGo_10.append(2)
                objDirection_10.append(2)
            elif whereToGo < 0.05:
                linkToGo_10.append(3)
                objDirection_10.append(2)
            elif whereToGo < 0.07:
                linkToGo_10.append(4)
                objDirection_10.append(2)
            elif whereToGo < 0.82:
                linkToGo_10.append(4)
                objDirection_10.append(0)
            elif whereToGo < 0.92:
                linkToGo_10.append(4)
                objDirection_10.append(1)
            elif whereToGo < 0.96:
                linkToGo_10.append(2)
                objDirection_10.append(1)
            else:
                linkToGo_10.append(1)
                objDirection_10.append(1)

    #print(arr_time10)
    #print(len(arr_time10))
    #print(linkToGo_10)
    #print(len(linkToGo_10))
    #print(objDirection_10)
    #print(len(objDirection_10))

    """
    			link	turn
    203	2%	2%	1	2
    206	2%	4%	2	2
    212	1%	5%	3	2
    213	2%	7%	4	2
    214	75%	82%	4	0
    215	10%	92%	4	1
    221	4%	96%	2	1
    222	4%	100%	1	1
    """



    ### Arrival time from 11 st
    t = 0
    while t < Sim_time:
        t += numpy.random.lognormal(lgm11, lgs11)
        if t < Sim_time:
            arr_time11.append(t)
    #print(arr_time11)


    ### Arrival time from 12 st
    t = 0
    while t < Sim_time:
        t += numpy.random.lognormal(lgm12, lgs12)
        if t < Sim_time:
            arr_time12.append(t)
    #print(arr_time12)


    ### Arrival time from 13 st
    t = 0
    while t < Sim_time:
        t += numpy.random.lognormal(lgm13, lgs13)
        if t < Sim_time:
            arr_time13.append(t)
    #print(arr_time13)
    return [arr_time10,arr_time11,arr_time12,arr_time13]

"""
for i in range(0,100):
    generate_time()
    print(arr_time10[0])
"""