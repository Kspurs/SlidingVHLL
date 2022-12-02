from vHLL import vHLL
import math
import mmh3
import random
class slidingvhll:
    def __init__(self,m,s,size):
        self.SLIDING_WINDOW_SIZE=size
        self.vHLLlist=[]
        self.randomNums=set()
        self.mergedvalues=[0]*m
        self.n=0
        self.s=s
        while (len(self.randomNums) < self.s):
            rad = random.randint(0, 2 ** 32 - 1)
            if (rad not in self.randomNums):
                self.randomNums.add(rad)
        self.randomNums=list(self.randomNums)
        self.m = m
        self.curvhll=vHLL(m,s,self.randomNums)
    def H(self,x):
        return mmh3.hash(str(x),0,signed=False)
    def update(self,f,e):
        self.curvhll.update(f,e)
    def ostrasize(self):
        if len(self.vHLLlist)<self.SLIDING_WINDOW_SIZE:
            self.vHLLlist.append(self.curvhll)
        else:
            self.vHLLlist.pop(0)
            self.vHLLlist.append(self.curvhll)
        self.curvhll=vHLL(self.m,self.s,self.randomNums)
    def merge(self):
        for vhll in self.vHLLlist:
            for i in range(self.m):
                self.mergedvalues[i]=max(self.mergedvalues[i],vhll.phyCounter[i])
        self.calN()
    def query(self,f):
        values=[]
        f32=self.H(f)
        for i in range(self.s):
            index=self.H(f32^self.randomNums[i])%self.m
            values.append(self.mergedvalues[index])
        ns=self.estimate(values)
        res = ns - self.s * self.n / self.m
        return max(res, 1)
    def estimate(self,values):
        s=len(values)
        a=0.7213/(1+1.079/s)
        sum_t=0.0
        zero=0
        for i in range(s):
            if values[i]==0:
                zero+=1
            sum_t+=1.0/pow(2,values[i])
        result=a*s*s/sum_t
        if result<2.5*s and zero>0:
            result=-s*math.log(zero/len(values))
        return result
    def calN(self):
        a = 0.7213 / (1 + 1.079 / self.m)
        sum_t = 0.0
        zero = 0
        for i in range(self.m):
            if self.mergedvalues[i] == 0:
                zero += 1
            sum_t += 2 ** -(self.mergedvalues[i])
        result = a * self.m**2 / sum_t
        if result < 2.5 * self.m and zero > 0:
            result = -self.m * math.log(zero / self.m)
        elif result> 2 ** 32 / 30:
            result=-2**32*math.log(1-result/2**32)
        self.n=result




