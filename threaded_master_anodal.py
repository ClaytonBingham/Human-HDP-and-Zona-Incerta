import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool 
import subprocess as sp
import os


def find_cell_threshold(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_anodal.py '+str(cellnum)+' '+str(electrode),shell=True)

def plot_cell_at_threshold(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_anodal.py '+str(cellnum)+' '+str(electrode)+' show 0.0',shell=True)

def plot_cell_at_fixed_amplitude(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_anodal.py '+str(cellnum)+' '+str(electrode)+' show '+str(1.5)+' fixed',shell=True)

#New
#10 - [3,12,18,21,24,37,39,46,47,48,49,52,58,64,65,68,70,72,74,88,93,96,99]
#8  - [3,12,18,20,21,24,37,39,42,46,47,48,49,52,58,64,65,68,70,72,74,75,81,88,93,96,99]
#6  - [0,1,3,7,12,15,18,19,20,21,23,24,25,26,32,33,37,38,39,41,42,46,47,48,49,50,52,58,60,64,65,67,68,70,72,73,74,75,81,82,85,87,88,90,93,94,96,99]
#4  - [0,1,2,3,4,5,6,7,8,9,11,12,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,67,68,69,70,71,72,73,74,75,76,78,79,81,82,83,85,86,87,88,89,90,91,93,94,96,97,99] 
# - [0.5,0.38,0.96,1.32,0.32,0.48,0.78,1.28,0.9,0.98,0.68,0.58,0.18,0.52,0.48,0.48,0.08,1.0,0.38,0.54,1.12,0.56,0.56,]
# - [0.98,0.58,1.24,0.08,1.7,0.68,0.64,1.04,1.52,1.16,1.28,0.82,0.68,0.36,0.72,0.74,0.62,0.34,1.26,0.52,0.18,0.12,0.74,1.4,0.66,0.84,]
# - [0.44,0.14,1.5,0.24,1.06,0.38,1.96,0.36,2.28,0.38,1.4,0.22,0.52,0.38,0.16,1.08,0.2,1.4,0.1,0.62,2.18,1.78,1.68,1.32,0.02,0.96,0.82,0.2,1.34,1.38,0.06,0.96,0.6,1.76,0.22,0.86,0.58,0.64,0.14,0.52,0.1,1.08,0.34,1.78,0.22,0.98,1.32]
# - [1.18,1.24,0.32,3.14,0.76,0.4,0.84,0.9,0.36,0.08,0.24,1.9,2.1,0.2,3.88,1.22,1.18,2.78,0.64,1.56,2.36,1.72,1.7,0.46,1.0,0.62,0.72,0.48,1.86,1.62,0.82,0.68,1.14,2.08,1.26,2.0,0.46,0.7,2.08,0.5,3.66,3.64,2.0,2.32,1.66,0.6,1.8,1.12,0.2,0.56,0.3,1.8,0.62,1.54,0.62,0.44,2.02,3.72,1.72,2.56,1.7,1.68,0.48,3.56,0.98,2.2,1.98,0.84,0.58,0.4,2.36,1.8,0.8,1.66,0.44,1.32,2.22,0.54,1.5,1.34,1.74,1.66,2.26,0.7,3.22]

#Petersen
#10 - [5,14,22,30,35,42,49,70,78,95,]
#8  - [2,5,14,16,22,26,30,35,42,43,49,70,78,95]
#6  - [0,1,2,5,6,8,14,16,22,26,28,30,35,42,43,48,49,56,64,66,70,74,78,80,86,90,91,95,96]
#4  - [0,1,2,3,5,6,8,13,14,16,17,20,21,22,23,25,26,28,29,30,33,34,35,38,39,42,43,44,45,46,47,48,49,50,52,53,54,56,57,61,62,63,64,65,66,67,68,70,74,75,78,79,80,82,83,86,87,88,90,91,92,93,95,96,98]
# - [0.62,0.24,0.34,1.0,0.6,0.74,0.5,0.04,0.74,0.78]
# - [0.06,0.78,0.44,0.2,0.48,0.16,1.26,0.76,0.92,0.14,0.66,0.18,0.92,0.88]
# - [0.72,0.08,0.46,1.18,0.24,0.22,1.06,0.58,0.82,0.52,0.04,1.74,1.18,1.4,0.5,0.18,1.04,0.14,0.38,0.32,0.6,0.34,1.38,0.34,0.1,0.38,0.26,1.16,0.22]
# - [1.74,1.12,1.86,0.62,2.74,0.74,1.44,0.36,1.74,0.54,0.36,1.36,0.94,1.96,1.24,1.82,0.92,1.4,3.56,0.76,1.18,2.36,0.96,0.8,2.26,1.66,1.44,0.42,1.3,0.14,1.54,2.56,0.8,0.26,1.06,1.1,1.8,0.52,0.32,0.08,0.86,2.02,0.62,1.52,0.16,0.74,1.62,1.66,1.12,2.4,1.14,1.1,1.1,1.56,1.76,0.48,0.54,1.86,1.6,0.84,2.32,2.0,2.16,0.94]

if __name__ == "__main__":
	estimate = False
	plot = False
	get_results=True
	numthreads = multiprocessing.cpu_count()
#	for diam in [10,8,6,4]:
#		os.rename(os.getcwd()+'/morphs_'+str(diam)+'um'+'/',os.getcwd()+'/morphs/')
#		electrode = 2
#		print('Starting electrode '+str(electrode))
#		if estimate:
#			with open(os.getcwd()+'/morphs/'+'multipro_anodal_thresholds.txt','w') as f:
#				pass
#			
#			pool = ThreadPool(numthreads)
#			pool.map(find_cell_threshold,list(zip(range(100),[diam for i in range(100)])))
#			pool.close()
#		
#		if plot:
#			for i in range(100):
#				plot_cell_at_threshold([i,diam])
#		
#		if get_results:
#			pool = ThreadPool(numthreads)
#			pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[diam for i in range(100)])))
#			pool.close()
#		
#		print('Finished bipolar electrode '+str(electrode))
#		os.rename(os.getcwd()+'/morphs/',os.getcwd()+'/morphs_'+str(diam)+'um'+'/')

#	if get_results:
#		input('move sptimes to correct folder and hit enter')
#	
#	for diam in [10,8,6,4]:
#		os.rename(os.getcwd()+'/petersen_morphs_'+str(diam)+'um'+'/',os.getcwd()+'/morphs/')
#		electrode = 2
#		print('Starting electrode '+str(electrode))
#		if estimate:
#			with open(os.getcwd()+'/morphs/'+'multipro_anodal_thresholds.txt','w') as f:
#				pass
#			
#			pool = ThreadPool(numthreads)
#			pool.map(find_cell_threshold,list(zip(range(100),[diam for i in range(100)])))
#			pool.close()
#		
#		if plot:
#			for i in range(100):
#				plot_cell_at_threshold([i,diam])
#		
#		if get_results:
#			pool = ThreadPool(numthreads)
#			pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[diam for i in range(100)])))
#			pool.close()
#		
#		print('Finished bipolar electrode '+str(electrode))
#		os.rename(os.getcwd()+'/morphs/',os.getcwd()+'/petersen_morphs_'+str(diam)+'um'+'/')
	
	
	for diam in [10,8,6,4]:
		os.rename(os.getcwd()+'/IC_morphs_'+str(diam)+'um'+'/',os.getcwd()+'/morphs/')
		electrode = 2
		print('Starting electrode '+str(electrode))
		if estimate:
			with open(os.getcwd()+'/morphs/'+'multipro_anodal_thresholds.txt','w') as f:
				pass
			
			pool = ThreadPool(numthreads)
			pool.map(find_cell_threshold,list(zip(range(100),[diam for i in range(100)])))
			pool.close()
		
		if plot:
			for i in range(100):
				plot_cell_at_threshold([i,diam])
		
		if get_results:
			pool = ThreadPool(numthreads)
			pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[diam for i in range(100)])))
			pool.close()
		
		print('Finished bipolar electrode '+str(electrode))
		os.rename(os.getcwd()+'/morphs/',os.getcwd()+'/IC_morphs_'+str(diam)+'um'+'/')
		
