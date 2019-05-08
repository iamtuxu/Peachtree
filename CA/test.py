import map_func
import Arr_Time
import stats
#import time
#import matplotlib.pyplot as plt

travelTime = []
avgSpeed = []
exit_rate = []
acc_TravelTimeList = [[],[]]

for i in range(100):
	Arr_Time.generate_time()

	[TravelTimeList,exit,spd,time] =  map_func.run_CA_on_peachtree(1800, Arr_Time.arr_time10,Arr_Time.linkToGo_10,Arr_Time.objDirection_10,Arr_Time.arr_time11,Arr_Time.arr_time12,Arr_Time.arr_time13)
	travelTime.append(time)
	avgSpeed.append(spd)
	exit_rate.append(exit/1800*3600)
	acc_TravelTimeList[0]=TravelTimeList[0]
	acc_TravelTimeList[1]=TravelTimeList[1]


# plt.plot(acc_TravelTimeList[1],acc_TravelTimeList[0])
# plt.axis([0, 1800, 0, 130])
# plt.xlabel('system time (sec)')
# plt.ylabel('average travel time (sec)')

plt.show()

m_time,h_time = stats.mean_confidence_interval(travelTime)
m_exit,h_exit = stats.mean_confidence_interval(exit_rate)
m_spd,h_spd = stats.mean_confidence_interval(avgSpeed)
print('Average time travel through: %.2f ± %.2f sec. Average flow rate: %.2f ± %.2f veh/hrs. Average speed:%.2f ± %.2f mph'%(m_time,h_time,m_exit,h_exit,m_spd * 11,h_spd*11))
