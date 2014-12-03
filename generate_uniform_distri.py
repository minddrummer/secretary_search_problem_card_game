# generate the uniform distribution for the experiment
# the values are 25,50,75,100,125,15 to 1000 so that (X-d)> 0, X is the mean,  d is the half range of the uniform distribution
import numpy as np


N = 12 # 12 distribution needed
#for integer value, arange is the same as range, for non-integer value, it is better to use linspace function
values_pool = np.arange(25, 1005, 25)

final_list = []
num_values = len(values_pool)

#in numpy, seed will make all the following random event predictable, which is cool; you donot have to reseed again if you are going to 
# do randomization for several times--all the following random events will be set.
np.random.seed(007)
i = 1
while i <= N:
	index_mean = np.random.randint(num_values)
	index_half_range = np.random.randint(num_values)
	while index_half_range >= index_mean:
		index_half_range = np.random.randint(num_values)

	para_values = (values_pool[index_mean], values_pool[index_half_range])
	if para_values not in final_list:
		final_list.append(para_values)
		i += 1

print final_list
#print len(final_list)
#print i















































