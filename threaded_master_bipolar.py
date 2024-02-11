import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool 
import subprocess as sp
import os


def find_cell_threshold(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_bipolar.py '+str(cellnum)+' '+str(electrode),shell=True)

def plot_cell_at_threshold(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_bipolar.py '+str(cellnum)+' '+str(electrode)+' show 0.0',shell=True)

def plot_cell_at_fixed_amplitude(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_bipolar.py '+str(cellnum)+' '+str(electrode)+' show '+str(1.0)+' fixed',shell=True)

#New
#10 - [3,4,9,12,15,18,20,21,23,25,35,36,37,39,42,44,46,47,48,49,52,58,64,65,68,72,73,74,88,93,96,99] #43,62,76,84,95,98,
#8  - [3,4,7,9,12,15,18,20,21,23,25,35,36,37,39,42,44,46,47,48,49,52,58,64,65,68,70,72,73,74,88,93,96,99]
#6  - [3,4,7,9,12,15,18,20,21,23,25,35,36,37,39,42,44,46,47,48,49,52,55,58,64,65,68,70,72,73,74,88,93,96,99]
#4  - [3,4,7,9,12,15,18,19,20,21,23,24,25,33,35,36,37,39,42,44,46,47,48,49,52,55,58,64,65,68,70,72,73,74,85,88,93,96,99]
# - [1.02,0.7,0.64,0.28,0.08,1.7,0.54,2.12,0.3,0.62,0.54,0.4,0.42,0.98,0.3,0.3,2.08,1.3,1.58,0.64,0.78,0.8,0.16,0.7,0.48,1.54,0.38,0.66,0.68,2.92,0.64,0.26]
# - [1.02,0.72,0.26,0.72,0.34,0.18,2.1,0.58,2.56,0.4,0.76,0.64,0.48,0.54,0.98,0.54,0.56,2.08,1.74,1.58,0.84,0.88,1.12,0.4,0.7,0.52,0.24,1.54,0.74,0.7,0.82,2.92,0.72,0.36]
# - [1.0,0.90,0.5,0.72,0.4,0.22,2.1,0.58,2.56,0.66,0.76,0.70,0.48,0.60,1.10,0.54,0.56,2.08,1.90,2.30,0.90,1.10,0.98,1.0,0.7,1.2,0.56,0.3,1.8,0.9,0.74,0.82,2.92,0.72,0.48]
# - [2.32,1.34,0.98,1.2,1.2,1.3,3.6,0.7,1.14,4.6,1.2,2.1,0.8,0.6,0.94,1.1,1.1,1.7,1.4,2.3,3.7,3.5,3.8,1.8,1.5,2.5,1.9,1.6,1.98,1.08,0.6,3.4,2.8,1.34,0.9,1.48,4.5,1.24,1.5]

#Petersen
#10 - [3,5,14,16,22,30,35,42,49,64,70,73,77,78,86,95]
#8  - [3,5,14,16,22,30,35,42,49,64,70,73,77,78,86,95]
#6  - [3,5,14,16,22,30,35,42,49,64,70,73,77,78,86,95]
#4  - [3,5,14,16,22,26,30,35,42,49,64,70,73,77,78,80,86,95,96]
# - [0.96,0.64,0.12,0.98,0.38,1.24,0.64,0.82,0.44,0.44,0.22,0.72,0.36,0.7,0.10,0.76]
# - [1.54,0.68,0.30,1.90,0.42,1.40,0.64,0.84,0.60,0.60,0.30,0.80,0.60,1.0,0.28,0.82]
# - [1.54,0.80,0.40,2.10,0.50,1.80,0.90,1.10,0.74,0.84,0.62,0.88,0.62,1.0,0.70,1.02]
# - [2.12,1.40,1.10,3.90,1.00,3.10,1.34,1.84,1.04,2.10,1.08,1.50,2.50,1.62,1.64,2.46,1.44,1.70]

if __name__ == "__main__":
	estimate = False
	plot = True
	get_results=False
	numthreads = multiprocessing.cpu_count()
	for diam in [10,8,6,4]:
		os.rename(os.getcwd()+'/morphs_'+str(diam)+'um'+'/',os.getcwd()+'/morphs/')
		electrode = 2
		print('Starting electrode '+str(electrode))
		if estimate:
			numthreads = multiprocessing.cpu_count()
			with open(os.getcwd()+'/morphs/'+'multipro_bipolar_thresholds.txt','w') as f:
				pass
			
			pool = ThreadPool(numthreads)
			pool.map(find_cell_threshold,list(zip(range(100),[diam for i in range(100)])))
			pool.close()
		
		if plot:
			for i in range(100):
				plot_cell_at_threshold([i,diam])
		
		if get_results:
	#		for i in range(100):
			pool = ThreadPool(numthreads)
			pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[diam for i in range(100)])))
			pool.close()
	#			plot_cell_at_fixed_amplitude([i,electrode])
		
		print('Finished bipolar electrode '+str(electrode))
		os.rename(os.getcwd()+'/morphs/',os.getcwd()+'/morphs_'+str(diam)+'um'+'/')

	if get_results:
		input('move sptimes to correct folder and hit enter')
	
	for diam in [10,8,6,4]:
		os.rename(os.getcwd()+'/petersen_morphs_'+str(diam)+'um'+'/',os.getcwd()+'/morphs/')
		electrode = 2
		print('Starting electrode '+str(electrode))
		if estimate:
			numthreads = multiprocessing.cpu_count()
			with open(os.getcwd()+'/morphs/'+'multipro_bipolar_thresholds.txt','w') as f:
				pass
			
			pool = ThreadPool(numthreads)
			pool.map(find_cell_threshold,list(zip(range(100),[diam for i in range(100)])))
			pool.close()
		
		if plot:
			for i in range(100):
				plot_cell_at_threshold([i,diam])
		
		if get_results:
	#		for i in range(100):
			pool = ThreadPool(numthreads)
			pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[diam for i in range(100)])))
			pool.close()
	#			plot_cell_at_fixed_amplitude([i,electrode])
		
		print('Finished bipolar electrode '+str(electrode))
		os.rename(os.getcwd()+'/morphs/',os.getcwd()+'/petersen_morphs_'+str(diam)+'um'+'/')
