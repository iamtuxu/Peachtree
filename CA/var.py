# direction

N = {0: [-1, 0], 1: None, 2: None, 3: None, 'sym':'↑','Lsym':'⇈'}
W = {0: None, 1: None, 2: None, 3: [0, -1], 'sym':'←','Lsym':'⇇'}
S = {0: None, 1: None, 2: [1, 0], 3: None, 'sym':'↓','Lsym':'⇊'}
E = {0: None, 1: [0, 1], 2: None, 3: None, 'sym':'→','Lsym':'⇉'}

NW = {0: [-1, 0], 1: None, 2: None, 3: [0, -1], 'sym':'↖'}
SW = {0: None, 1: None, 2: [1, 0], 3: [0, -1], 'sym':'↙'}
SE = {0: None, 1: [0, 1], 2: [1, 0], 3: None, 'sym':'↘'}
NE = {0: [-1, 0], 1: [0, 1], 2: None, 3: None, 'sym':'↗'}

X = 'X'

speedtable = {0:2, 1:3, 2:3, 3:4, 4:4}