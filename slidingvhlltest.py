from slidingvHLL_revised import slidingvhll
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
svhll=slidingvhll(2**20,256,5)
row_second=len(readdata)//60
while i <=row_second*5:
    row = readdata[i].strip()
    if row[0] == 'a':
        i += 1
        continue
    src = row.split(" ")[1]
    dst = row.split(" ")[0]
    if src not in flow_cardinality:
        flow_cardinality[src] = set()
    flow_cardinality[src].add(dst)
    svhll.update(src, dst)
    if i%row_second==0:
        svhll.ostrasize()
    i+=1
svhll.merge()
x = []
y = []
are=0
flows=0
for key in flow_cardinality:
    es = svhll.query(key)
    ac = len(flow_cardinality[key])
    are+=abs(es-ac)/ac
    flows+=1
    x.append(ac)
    y.append(es)
draw(x, y)
print(flows)
print(are/flows)