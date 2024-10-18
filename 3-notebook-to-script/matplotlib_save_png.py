import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Simple Plot')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()

plt.savefig('simple_plot.png')
