# 6730Project2
## Quickstart
### Environment requirement on PACE
All our simulation is tested on PACE using module `anaconda3`. To load this module, run 
```
module load anaconda3
``` 
on the shell of PACE.

### Start Simulation
#### Event-oriented Simulation
Run from `./EO` directory  
```
python mainSim.py
``` 
to start.  
The above script will run simulation 100 time with random generated vehicle. The generated vehicle will following lognormal distribution.  
The script will output 95% confidence interval of average travel time, average speed of each vehicle and vehicle flow rate. The result will be printed to the shell.

#### Cellular Automata
Run from `./CA` directory
```
python test.py
```  
to start.  
The above script will run simulation 100 time with random generated vehicle. The generated vehicle will following lognormal distribution.  
The script will output 95% confidence interval of average travel time, average speed of each vehicle and vehicle flow rate. The result will be printed to the shell.

#### Activity Scanning Simulation
Run from `./AS` directory
```
python Simulation.py
```   
to start.  
The above script will run simulation 100 time with random generated vehicle. The generated vehicle will following lognormal distribution.  
The script will output 95% confidence interval of average travel time, average speed of each vehicle and vehicle flow rate. The result will be printed to the shell.

## Detailed code usage 
### Random vehicle generator
The `Arr_time.py` is a random vehicle generator.   
Under the function definition, the parameter of lognormal distribution can be found as:
```
    lgm10 = 1.18642284
    lgs10 = 1.07569549
    lgm11 = 5.6638771
    lgs11 = 0.2979011
    lgm12 = 3.7199815
    lgs12 = 1.9696008
    lgm13 = 3.661255
    lgs13 = 1.1952896
```
Those parameter can be edit to simulate different traffic load. A separate `Arr_time.py` can be found in each simulation folder. 
#### Output
The generator will output:  
`arr_time10` is a list of time of each vehicle entering the system on 10th street in second  
`linkToGo_10` is a list of corresponding target link. Each vehicle in `arr_time10` should have a corresponding value in this list. Possible value are `1`,`2`,`3`,`4`, which indicate that the vehicle is exit at 11th, 12th, 13th, 14th, respectively.  
`objDirection_10` is list of direction where the vehicle is exiting. Possible value are `0`,`1`,`2` which indicate go stright, left turn, right turn, respectively.  
`arr_time11` is a list of time of each vehicle entering the system on 11th street in second
`arr_time12` is a list of time of each vehicle entering the system on 12th street in second
`arr_time13` is a list of time of each vehicle entering the system on 13th street in second

All lists above can be used as a input of all 3 simulation. 

### Event-Oriented Simulation
#### Commented section
The code used to calculate Warm-up time and V&V result is commented. The instruction to enable them are in the report.

### Cellular Automata
#### Constructed map
`map_func.py` contains the constructed map for 10-14 th street and peachtree street. 
#### Run custom simulation
To run simulation on the map, simply import `map_func.py` call  
```
run_CA_on_peachtree(simitime,arr_time10,linkToGo_10,objDirection_10,arr_time11,arr_time12,arr_time13):
``` 
with desired value. This will output average travel time, average speed of each vehicle and vehicle flow rate by printing on shell.
#### Custom map
Detailed custom map instruction can be found in `./CA/README.md`


### Activity Scanning Model
#### Network visualization
All the vehicles in the system can be printed at any given time. 
#### Warmup Period
The simulation can plot the current system preproity to identify warmup period. 