import numpy as np
from var import *
import time
#import matplotlib.pyplot as plt


class map(object):
	def __init__(self, input_arr):
		self.cellmap = input_arr
		self.max_y = len(input_arr)
		self.max_x = len(input_arr[0])
		self.systime = 0
		self.spawncount = 0
		self.exitcount = 0
		self.acc_exit_veh_count = 0
		self.main_exit_veh_count = 0
		self.main_exit_time_count = 0
		self.speedcount = 0
		self.speedsum = 0

	def put_car(self, coordy, coordx, car):
		self.cellmap[coordy][coordx].add_car(car)

	def update(self):
		self.systime += 1
		ref_cellmap = self.construct_ref()
		#print(ref_cellmap)
		# set all cars unmoved.
		for y in range(self.max_y):
			for x in range(self.max_x):
				cell = self.cellmap[y][x]
				if cell != X:  # is a road
					if cell.car:  # has a car
						cell.car.moved = False

		for y in range(self.max_y):
			for x in range(self.max_x):
				cell = self.cellmap[y][x]
				if cell != X:  # is a road
					if cell.car:  # has a car, hasn't moved
						self.speedsum += cell.car.speed
						self.speedcount += 1
						if cell.car.moved:
							continue
						cell.car.moved = True
						cell.car.time_elapsed += 1
						last_see_turn = cell.car.see_turn
						if cell.car.comm != cell.car.direction and cell.car.delay == 0: #cars needs turn
							##get pd
							pd = 0
							for i in range(9):
								scan_y = y + cell.dir[cell.car.direction][0] * (i + 1)
								scan_x = x + cell.dir[cell.car.direction][1] * (i + 1)
								if scan_x < self.max_x and scan_y < self.max_y:
									seeing_car = ref_cellmap[scan_y][scan_x]
								else:
									seeing_car = -1
								pd = i
								if seeing_car in [0,1,2,3,4]:
									pd = pd + seeing_car
									break
								elif seeing_car in [9,10,11,12,13,14]:
									pd = pd + 1
									break
						else: #cars does not need turn
							## get Pd
							pd = 0
							cell.car.see_turn = False
							for i in range(9):
								scan_y = y + cell.dir[cell.car.direction][0] * (i + 1)
								scan_x = x + cell.dir[cell.car.direction][1] * (i + 1)
								if scan_x < self.max_x and scan_y < self.max_y:
									seeing_car = ref_cellmap[scan_y][scan_x]
								else:
									seeing_car = -1
								pd = i
								if seeing_car in [9,10,11,12,13,14]:
									cell.car.see_turn = True
								elif cell.car.see_turn == True:
									pass
								else:
									cell.car.see_turn = False

								if seeing_car in [0,1,2,3,4]:
									pd = pd + seeing_car
									break
								elif seeing_car in [10,11,12,13,14]:
									pd = pd + seeing_car-10
									break


						cell.car.pd = pd
						#calculate speed
						cell.car.speed = min(self.acc(cell.car.speed), self.dcc(cell.car.pd))

						if cell.dir[cell.car.comm] == None:  # can not execute turn
							ny = y + cell.dir[cell.car.direction][0]*cell.car.speed
							nx = x + cell.dir[cell.car.direction][1]*cell.car.speed
						elif cell.car.delay == 0:
							ny = y + cell.dir[cell.car.comm][0]*cell.car.speed
							nx = x + cell.dir[cell.car.comm][1]*cell.car.speed
						else:
							ny = y + cell.dir[cell.car.direction][0] * cell.car.speed
							nx = x + cell.dir[cell.car.direction][1] * cell.car.speed

						cell.car.delay = cell.car.last_delay

						if last_see_turn != cell.car.see_turn and last_see_turn == True:
							cell.car.last_delay -= 1


						if nx < 0 or nx > self.max_x - 1:
							if cell.car.is_original == 1:
								self.main_exit_veh_count += 1
								self.main_exit_time_count += cell.car.time_elapsed
							cell.pop_car()
						elif ny < 0 or ny > self.max_y - 1: # go out of map
							cell.pop_car()
							self.acc_exit_veh_count += 1
						else:
							next_cell = self.cellmap[ny][nx]
							ref_next_cell = ref_cellmap[ny][nx]
							if ref_next_cell in [-1,9]:
								move_car = cell.pop_car()
								next_cell.add_car(move_car)



					if cell.spawn != None:  # is a spawn point
						if cell.spawncounter != 0:  # not yet the time
							cell.spawncounter -= 1
						else:  # it's the time
							refmap_spawn = self.construct_ref()
							if refmap_spawn[y][x] == -1:
								if cell.spawnarray_cur > len(cell.spawn_array) -1:
									cell.spawnarray_cur = 0

								cell.spawncounter = cell.spawn_array[cell.spawnarray_cur]
								cell.spawnarray_cur += 1

								if cell.spawnarray_cur > len(cell.spawn_array) -1:
									cell.spawnarray_cur = 0

								#spawncomm = np.random.choice(['L', 'R', 'D'], 1, p=[cell.Lrate, cell.Rrate, cell.Drate])
								#put_car(self, coordy, coordx, car):
								#__init__(self, comm, delay, direction, speed = 0):
								if cell.spawn_at_orig:
									self.put_car(y, x, car(cell.spawn_comm_array[cell.spawnarray_cur], cell.spawn_delay_array[cell.spawnarray_cur], cell.spawndir,0, fromorigin=1 ))
								else:
									self.put_car(y, x, car(cell.spawn_comm_array[cell.spawnarray_cur],cell.spawn_delay_array[cell.spawnarray_cur], cell.spawndir, 0))
								self.spawncount += 1

					if cell.trafficlight:
						#change state:
						if cell.trafficlight_counter != 0:
							cell.trafficlight_counter -= 1
						else:
							if cell.trafficlight_stat == True:
								cell.trafficlight_stat = False
								cell.trafficlight_counter = cell.trafficlight_stop_period
							else:
								cell.trafficlight_stat = True
								cell.trafficlight_counter = cell.trafficlight_go_period



	def acc(self,oldspeed):
		speedtable = {0: 2, 1: 3, 2: 3, 3: 4, 4: 4}
		return speedtable[oldspeed]
	def dcc(self,pd):
		if pd > 8:
			pd = 8
		speedtable = {8:4,7:3,6:3,5:3,4:2,3:2,2:1,1:1,0:0}
		return speedtable[pd]


	def construct_ref(self):
		ref_cellmap = []
		for item in self.cellmap:
			ref_cellmap.append(item.copy())
		for y in range(self.max_y):
			for x in range(self.max_x):
				cell = self.cellmap[y][x]
				if cell != X:  # is a road
					if cell.trafficlight:
						if cell.trafficlight_stat == False:
							ref_cellmap[y][x] = 0
						else:
							if cell.car == None:
								ref_cellmap[y][x] = -1
							else:
								ref_cellmap[y][x] = cell.car.speed
					elif not cell.dir_stright:
						if cell.car == None:
							ref_cellmap[y][x] = 9
						else:
							ref_cellmap[y][x] = cell.car.speed + 10
					else:
						if cell.car == None:
							ref_cellmap[y][x] = -1
						else:
							ref_cellmap[y][x] = cell.car.speed
		return ref_cellmap

	# def update_and_plot(self, n_iter):
	#
	# 	# plt.ion()
	# 	plt.ion()
	# 	for _ in range(n_iter):
	# 		self.update()
	# 		plot_cellmap = np.zeros((self.max_y, self.max_x))
	# 		for y in range(self.max_y):
	# 			for x in range(self.max_x):
	# 				cell = self.cellmap[y][x]
	# 				if cell != X:  # is a road
	# 					if cell.car:  # has a car
	# 						plot_cellmap[y, x] = 2
	# 					else:
	# 						plot_cellmap[y, x] = 1
	#
	# 		plt.title('Iter :{}'.format(self.systime))
	# 		plt.imshow(plot_cellmap)
	# 		plt.pause(0.2)
	# 	plt.ioff()

	# def plot(self):
	# 	plot_cellmap = np.zeros((self.max_y, self.max_x))
	# 	for y in range(self.max_y):
	# 		for x in range(self.max_x):
	# 			cell = self.cellmap[y][x]
	# 			if cell != X:  # is a road
	# 				if cell.car:  # has a car
	# 					plot_cellmap[y, x] = 2
	# 				else:
	# 					plot_cellmap[y, x] = 1
	# 	plt.imshow(plot_cellmap)
	# 	plt.show()


	def __str__(self):
		out = ''
		for row in self.cellmap:
			for item in row:
				out += ''
				out += str(item)
			out += '\n'
		return out


class road(object):
	def __init__(self, dir, spawn=None, spawnarray = None, spawncommarray = None, spawndelayarray = None, spawndir=None, spawnatorig = None, trafficlight=None, trafficlight_stop=0, trafficlightinit = True):
		self.car = None
		self.dir = dir
		self.dir_str = dir['sym']
		if self.dir in [N,W,S,E]:
			self.dir_stright = 1
		else:
			self.dir_stright = None

		self.spawn = spawn

		if spawn != None:
			self.spawnarray_cur = 1
			self.spawn_array = spawnarray
			self.spawn_comm_array = spawncommarray
			self.spawn_delay_array = spawndelayarray

			self.spawncounter = spawnarray[0]

			self.spawn_at_orig = spawnatorig
			# if LRlane == 'L':
			# 	self.Lrate = 0.4
			# 	self.Rrate = 0.0
			# 	self.Drate = 0.6
			# elif LRlane == 'R':
			# 	self.Lrate = 0.0
			# 	self.Rrate = 0.4
			# 	self.Drate = 0.6

			self.spawndir = spawndir

		self.trafficlight = trafficlight


		if trafficlight:
			self.dir_str = dir['Lsym']
			self.trafficlight_stat = trafficlightinit
			self.trafficlight_go_period = trafficlight
			self.trafficlight_stop_period = trafficlight_stop
			self.trafficlight_counter = trafficlight

	def add_car(self, car):
		if self.car:
			raise ValueError('already has car here!')
		else:
			self.car = car

	def pop_car(self):
		out = self.car
		self.car = None
		return out

	def __str__(self):
		if self.car == None:
			return self.dir_str
		else:
			#return str(self.car.comm) +'/'+ str(self.car.direction) + '/' + str(self.car.pd)
			return str(self.car.speed)
		# return str(self.car)


class car(object):
	def __init__(self, comm, delay, direction, speed = 0, fromorigin = 0):
		self.direction = direction
		if comm == 'L':
			self.comm = (direction - 1) % 4
		if comm == 'R':
			self.comm = (direction + 1) % 4
		elif comm == 'D':
			self.comm = direction
		self.delay = delay
		self.last_delay = delay
		self.moved = False
		self.speed = speed
		self.pd = 0
		self.time_elapsed = 0
		self.is_original = fromorigin
		self.need_turn = False
		self.see_turn = False

	def __str__(self):
		return '1'


# dy,dx
# if __name__ == '__main__':
# 	from var import *
#
# 	localmap = []
# 	bk = []
# 	for i in range(30):
# 		localmap.append(road(E))
# 		bk.append(X)
# 	localmap = [localmap] + [bk]
#
# 	game = map(localmap)
# 	game.put_car(0, 0, car('D', 0, 1, 2))
# 	for i in range(30):
# 		print(i, end=':')
# 		print(game)
# 		game.update()
# 		time.sleep(0.2)
# 	input_map = [[X, X, road(N), X, X],
# 				 [X, X, road(N), X, X],
# 				 [road(W), road(W), road(NW), X, X],
# 				 [X, X, road(N), X, X],
# 				 [X, X, road(N, 2, 0), X, X]]
#
# 	input_map = [[X, X, X, road(S, 1, 2, spawndelay=4), road(N), X, X, X],
# 				 [X, X, X, road(S), road(N), X, X, X],
# 				 [X, X, X, road(S), road(N), X, X, X],
# 				 [road(W), road(W), road(W), road(SW), road(NW), road(W), road(W), road(W, 1, 3)],
# 				 [road(E, 1, 1), road(E), road(E), road(SE), road(NE), road(E), road(E), road(E)],
# 				 [X, X, X, road(S), road(N), X, X, X],
# 				 [X, X, X, road(S), road(N), X, X, X],
# 				 [X, X, X, road(S), road(N, 1, 0), X, X, X]
# 				 ]
#
# 	# input_map = [[X, X, X, road(S, 0, 2), road(N), X, X, X],
# 	# 			 [X, X, X, road(S), road(N), X, X, X],
# 	# 			 [X, X, X, road(S,trafficlight=10,trafficlight_stop=10,trafficlightinit=True), road(N), X, X, X],
# 	# 			 [road(W), road(W), road(W), road(SW), road(NW), road(W,trafficlight=10,trafficlight_stop=10,trafficlightinit=False), road(W), road(W, 0, 3)],
# 	# 			 [road(E, 0, 1), road(E), road(E,trafficlight=10,trafficlight_stop=10,trafficlightinit=False), road(SE), road(NE), road(E), road(E), road(E)],
# 	# 			 [X, X, X, road(S), road(N,trafficlight=10,trafficlight_stop=10,trafficlightinit=True), X, X, X],
# 	# 			 [X, X, X, road(S), road(N), X, X, X],
# 	# 			 [X, X, X, road(S), road(N, 0, 0), X, X, X]
# 	# 			 ]
#
# 	input_map = [[X, X, X, road(S,0,2), road(N), X, X, X],
# 				 [X, X, road(S), road(SW), road(N), X, X, X],
# 				 [X, X, road(S), road(S, trafficlight=10, trafficlight_stop=10, trafficlightinit=True), road(N), road(W), road(W), X],
# 				 [road(W), road(W), road(W), road(SW), road(NW),road(W, trafficlight=10, trafficlight_stop=10, trafficlightinit=False), road(NW), road(W,1,3)],
# 				 [road(E,1,1), road(SE), road(E, trafficlight=10, trafficlight_stop=10, trafficlightinit=False),road(SE), road(NE), road(E), road(E), road(E)],
# 				 [X, road(E), road(E), road(S), road(N, trafficlight=10, trafficlight_stop=10, trafficlightinit=True), road(N), X, X],
# 				 [X, X, X, road(S), road(NE), road(N), X, X],
# 				 [X, X, X, road(S), road(N, 0, 0), X, X, X]
# 				 ]
#
#
#
#
# 	game = map(input_map)
# 	# game.update_and_plot(50) # How many iters you want to stimulate
#
#
# 	for x in range(50):
# 		game.update()
# 		print(game)
# 		time.sleep(0.2)
# while True:
# 		game.update()
# 		print(game)
#
# 		time.sleep(0.5)
