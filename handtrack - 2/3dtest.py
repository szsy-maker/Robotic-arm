import matplotlib.pyplot as plt
import numpy as np
import random

#3d

listx= [random.randint(0,100) for i in range(10)]
listy= [random.randint(0,100) for i in range(10)]
listz= [random.randint(0,100) for i in range(10)]

colors = np.random.rand(10)

fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(1,1,1,projection = "3d")
xpoints = np.array([0, 100,100])
ypoints = np.array([0, 100,100])
zpoints = np.array([0,100,-100])
ax1.scatter(listx, listy,listz,marker='o', s=100,c=colors)
#ax1.plot(listx, listy,listz,label = "3d curve")
ax1.legend()
plt.show()

list_x=[]
for i in range(20):
    list_x.append(0)
print(list_x)