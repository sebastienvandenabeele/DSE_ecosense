import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

x = np.linspace(0, 1000, 10000)
c0 = 10

norm = stats.norm.pdf(x, loc=300, scale=1)

plt.plot(x, norm)
plt.show()
