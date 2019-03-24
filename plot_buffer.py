import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    buf = np.load('buf.npy')
    ax1.clear()
    ax1.plot(buf)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()