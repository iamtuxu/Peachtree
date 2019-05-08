#Cellular Automata
##Custom Map Usage
#### Draw map
The map is a 2D array implemented by list in list. Each item in the array could be nothing or a road block. All road block requires a direction. You can also made a road block with traffic light or vehicle spawn function by adding optional argument.
#### Run automata
Simply call `.update()` function on map object to calculate the state of next step.
#### Map visualization
Use native python `print()` function on map object can visualize the map. Here is a example:
```
→	→	→	2	→	→	→	→	→	→
X	X	X	X	X	X	X	X	X	X
```
`X` : cell with nothing.   
`→` : empty road block. Arrow direction represent road direction.  
`2` : a vehicle in road block. It will travel at speed of 2 in next step. 
#### Simple example for one straight lane
First, draw map:
```
#create a list with 30 road object 
for i in range(30):
	localmap.append(road(E))
localmap = [localmap]
```
create map object:
```
game = map(localmap)
print(game)
```
we got our map as :
```
→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→
```
Then, put a car in the first cell:
```
game.put_car(0,0,car('D',0,1,0))
print(game)
```
The map was now like:
```
0	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→
```
Then, update the map 10 time and see what's happen:
```
for i in range(10):
	print(i, end= ':')
	print(game)
	game.update()
	time.sleep(0.2)
```
The result is:
```
0:	0	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→

1:	2	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→

2:	→	→	3	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→

3:	→	→	→	→	→	4	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→

4:	→	→	→	→	→	→	→	→	→	4	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→

5:	→	→	→	→	→	→	→	→	→	→	→	→	→	4	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→

6:	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	4	→	→	→	→	→	→	→	→	→	→	→	→

7:	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	4	→	→	→	→	→	→	→	→

8:	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	4	→	→	→	→

9:	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	→	4
```
