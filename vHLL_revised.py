from mmhash import mmhash
from murmurhash2 import murmurhash3
import mmh3
import math
import random
class vHLL:
    def __init__(self,physical_counter_num,virtual_counter_num,randomNums):
        self.phyCounter=[0 for i in range(physical_counter_num)]
        self.m=physical_counter_num #物理寄存器大小
        self.s=virtual_counter_num #每条流虚拟寄存器数量
        self.n=0 #通过self.estimate(self.phyCounter)得到的用于去噪的n
        self.r=randomNums #用于哈希函数的随机数组
        self.alpha = 0
        if self.s == 16:
            self.alpha = 0.673
        elif self.s == 32:
            self.alpha = 0.697
        elif self.s == 64:
            self.alpha = 0.709
        else:
            self.alpha = (0.7213 / (1 + (1.079 / self.s)))
    def H(self,x):
        return mmh3.hash(str(x),0,signed=False)
    def update(self,f,e):
        e32=self.H(e)
        f32=self.H(f)
        binarystring=[]  #计算哈希值的32位
        for i in range(32):
            if (e32>>i)&1:
                binarystring.append(1)
            else:
                binarystring.append(0)
        binarystring.reverse()
        b=int(math.log2(self.s))
        vCounterIndex=(e32>>(32-b))%(self.s//2)
        if e32*4>2**32-1:
            vCounterIndex+=self.s//2
        phyCounterIndex=self.H(f32^self.r[vCounterIndex])%self.m
        leadingZero=0
        for i in range(b,32):
            leadingZero+=1
            if binarystring[i]==1:
                break
        self.phyCounter[phyCounterIndex]=max(self.phyCounter[phyCounterIndex], leadingZero)
    def query(self,f):
        values=[]
        f32=self.H(f)
        for i in range(self.s):
            index=self.H(f32^self.r[i])%self.m
            values.append(self.phyCounter[index])
        ns=self.estimate(values)
        res=ns-self.s*self.n/self.m
        return max(res,1)
    def estimate(self,values):
        s=len(values)
        sum_t=0.0
        zero=0
        for i in range(s):
            if values[i]==0:
                zero+=1
            sum_t+=2**-(values[i])
        result=self.alpha*s*s/sum_t
        if result<2.5*s and zero>0:
            result=-s*math.log(zero/s)
        return result
    def calN(self):
        sum_t = 0.0
        zero = 0
        for i in range(self.m):
            if self.phyCounter[i] == 0:
                zero += 1
            sum_t += 2 ** -(self.phyCounter[i])
        result = self.alpha * self.m**2 / sum_t
        if result < 2.5 * self.m and zero > 0:
            result = -self.m * math.log(zero / self.m)
        self.n=result




