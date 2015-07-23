#write a script called "prob.py" that outputs frequencies, as well as creates
#and saves a boxplot, a histogram and a QQ-plot for the data in this lesson.

import collections
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt 

list_b = [1,1,1,1,1,1,1,1,2,2,2,3,4,4,4,4,5,6,6,6,7,7,7,7,7,7,7,7,8,8,9,9]


#list frequencies
d = collections.Counter(list_b)

count_sum = sum(d.values())

for k,v in d.iteritems():
	print "The frequency of number " + str(k) + "is " + str(float(v)/count_sum)

#output a boxplot
plt.boxplot(list_b)
plt.show()
plt.savefig("boxplot.png")

#output a histogram
plt.hist(list_b, histtype='bar')
plt.show()
plt.savefig("histogram.png")

#output a qq plot
raph1 = stats.probplot(list_b, dist = "norm", plot = plt)
plt.show() #generates a graph
plt.savefig("qqnorm.png")