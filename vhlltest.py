import random
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from vHLL import vHLL
matplotlib.rc("font", family="Microsoft YaHei")


def draw(x, y):
    x = np.array(x)
    y = np.maximum(1, np.array(y))
    x1 = range(0, 5)
    y1 = x1

    plt.plot(np.log10(x), np.log10(y), "x")
    plt.plot(x1, y1)
    plt.show()



data = open("C:\\Users\\ljc\\桌面\\file\\data.txt")
readdata = data.readlines()
data.close()
flow_cardinality = {}
i = 0
randNums=set()
while(len(randNums)<64):
    rad=random.randint(0,2**32-1)
    if(rad not in randNums):
        randNums.add(rad)
randNums=list(randNums)
vhll=vHLL(int(0.25 * 2 ** 23 / 5),64,randNums)
while i <len(readdata):
    row = readdata[i].strip()
    if row[0] == 'a':
        i += 1
        continue
    src = row.split(" ")[1]
    dst = row.split(" ")[0]
    if src not in flow_cardinality:
        flow_cardinality[src] = set()
    flow_cardinality[src].add(dst)
    vhll.update(src, dst)
    i += 1
vhll.calN()
print(vhll.n)
x = []
y = []
are=0
flows=0
for key in flow_cardinality:
    es = vhll.query(key)
    ac = len(flow_cardinality[key])
    are+=abs(es-ac)/ac
    flows+=1
    x.append(ac)
    y.append(es)
draw(x, y)
print(flows)
print(are/flows)
