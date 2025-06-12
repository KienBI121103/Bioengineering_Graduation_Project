import matplotlib.pyplot as plt

#Import input
x = ['ST2', 'ST571', 'ST1411', 'ST164', 'ST1412']
y = [6,2,1,1,1]
#Visualization
plt.bar(x,y)
plt.xlabel("ST")
plt.ylabel("Frequency")
plt.title("Number of ST")
plt.savefig("ST.png", dpi = 300)

plt.show()