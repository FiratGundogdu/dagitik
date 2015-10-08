
import numpy
import matplotlib.pyplot as plt

m1 = -3
s1 = 1
m2 = 5
s2 = 0.5

print "mu 1 = " , m1
print "sigma 1 = " , s1
print "mu 2 = " , m2
print "sigma 2 = " , s2


a1 = numpy.random.normal(m1,s1,10000)
a2 = numpy.random.normal(m2,s2,10000)

print "random array1= ",a1
print "random array2= ",a2

count1 = 0
count2 = 0

h1 = [0.0]*41 #histogram1
h2 = [0.0]*41 #histogram2


#histograma yerlestirme
for i in range(len(a1)):
    a1[i]=round(a1[i])
    if a1[i]<=20 and a1[i]>=-20:
        count1+=1
        h1[int(a1[i])+20]+=1

for n in range(len(a2)):
    a2[n]=round(a2[n])
    if a2[n]<=20 and a2[n]>=-20:
        count2+=1
        h2[int(a2[n])+20]+=1

print "histogram1= ", h1
print "histogram2= ", h2


#normalizasyon
for x in range(len(h1)):
    h1[x]=h1[x]/count1

for y in range(len(h2)):
    h2[y]=h2[y]/count2

print "normalize histogram1= ",h1
print "normalize histogram2=", h2

#plot
plt.axis((-20,20,0,1))
plt.bar(range(-20,21), h1,color='blue')
plt.bar(range(-20,21), h2,color='red')
plt.show()


#distance
i = 0
j = 0
sum=0

while(i<40 and j<40):
    if h1[i] == 0:
        i+=1
        continue

    if h2[j] == 0:
        j+=1
        continue

    if h1[i]<h2[j]:
        sum=sum+h1[i]*abs(i-j)
        h1[i]=0
        h2[j]=h2[j]-h1[i]
        continue

    if h1[i]>=h2[j]:
        sum=sum+h1[j]*abs(i-j)
        h2[j]=0
        h1[i]=h1[i]-h2[j]
        continue

print "distance= ",sum

















