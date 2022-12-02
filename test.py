N,K=map(int,input().split())
re={}
bo={}
lst=[1]*N
keys={}
for i in range(1,N+1):
	keys[i]=i-1
for i in range(K):
	s,w,c=map(int,input().split())
	if w+c not in re:
		re[w+c]=[]
	re[w+c].append(s)
	if w not in bo:
		bo[w]=[]
	bo[w].append(s)
for i in range(10500):
	if i in re:
		re[i].sort()
		j=0
		for k in re[i]:
			while lst[j]==1:
				j+=1
			lst[j]=1
			keys[k]=j
	if i in bo:
		for k in bo[i]:
			lst[keys[k]]=0
ans=[""]*N
for i in range(N):
	ans[keys[i+1]]=str(i+1)
print(" ".join(ans))
