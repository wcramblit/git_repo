# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 21:03:56 2015

@author: wcramblit
"""

import random
import numpy as np
import matplotlib.pyplot as plt

# normally distributed values
norm_dist = [random.choice(np.random.normal(0, 1, 1000)) for i in range(1000)]

# track max and mins
maximums = [np.amax(np.random.normal(0, 1, 1000)) for i in range(1000)]
minimums = [np.amin(np.random.normal(0, 1, 1000)) for i in range(1000)]

# distribution of samples is normal
plt.hist(norm_dist, histtype='bar')
plt.show()
plt.clf()

# distribution of max and min are normal but to each side
plt.hist(maximums, histtype='bar', label='max vals')
plt.hist(minimums, histtype='bar', label='min vals')
plt.show()