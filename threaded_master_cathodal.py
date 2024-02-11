import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool 
import subprocess as sp
import os


def find_cell_threshold(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_cathodal.py '+str(cellnum)+' '+str(electrode),shell=True)

def plot_cell_at_threshold(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_cathodal.py '+str(cellnum)+' '+str(electrode)+' show 0.0',shell=True)

def plot_cell_at_fixed_amplitude(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_cathodal.py '+str(cellnum)+' '+str(electrode)+' show '+str(1.0)+' fixed',shell=True)

#1 - []
#2 - []
#3 - []
#4 - []


if __name__ == "__main__":
	estimate = False
	plot = False
	get_results=True
	numthreads = multiprocessing.cpu_count()
#	electrode = 1
#	print('Starting electrode '+str(electrode))
#	if estimate:
#		numthreads = multiprocessing.cpu_count()
#		with open('multipro_contact'+str(electrode)+'_thresholds.txt','w') as f:
#			pass
#		
#		pool = ThreadPool(numthreads)
#		pool.map(find_cell_threshold,list(zip(range(100),[electrode for i in range(100)])))
#		pool.close()
#	
#	if plot:
#		for i in range(100):
#			plot_cell_at_threshold([i,electrode])
#	
#	print('Finished electrode '+str(electrode))
#	
#	electrode = 2
#	print('Starting electrode '+str(electrode))
#	if estimate:
#		numthreads = multiprocessing.cpu_count()
#		with open(os.getcwd()+'/morphs/'+'multipro_contact'+str(electrode)+'_thresholds.txt','w') as f:
#			pass
#		
#		pool = ThreadPool(numthreads)
#		pool.map(find_cell_threshold,list(zip(range(100),[electrode for i in range(100)])))
#		pool.close()
#	
#	if plot:
#		for i in range(100):
#			plot_cell_at_threshold([i,electrode])
#	
#	if get_results:
##		for i in range(100):
#		pool = ThreadPool(numthreads)
#		pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[electrode for i in range(100)])))
#		pool.close()
##			plot_cell_at_fixed_amplitude([i,electrode])
#	
#	print('Finished electrode '+str(electrode))
#	
#	electrode = 3
#	print('Starting electrode '+str(electrode))
#	if estimate:
#		numthreads = multiprocessing.cpu_count()
#		with open(os.getcwd()+'/morphs/'+'multipro_contact'+str(electrode)+'_thresholds.txt','w') as f:
#			pass
#		
#		pool = ThreadPool(numthreads)
#		pool.map(find_cell_threshold,list(zip(range(100),[electrode for i in range(100)])))
#		pool.close()
#	
#	if plot:
#		for i in range(100):
#			plot_cell_at_threshold([i,electrode])
#	
#	if get_results:
##		for i in range(100):
#		pool = ThreadPool(numthreads)
#		pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[electrode for i in range(100)])))
#		pool.close()
##			plot_cell_at_fixed_amplitude([i,electrode])
#	
#	print('Finished electrode '+str(electrode))
#	
#	electrode = 4
#	print('Starting electrode '+str(electrode))
#	if estimate:
#		numthreads = multiprocessing.cpu_count()
#		with open(os.getcwd()+'/morphs/'+'multipro_contact'+str(electrode)+'_thresholds.txt','w') as f:
#			pass
#		
#		pool = ThreadPool(numthreads)
#		pool.map(find_cell_threshold,list(zip(range(100),[electrode for i in range(100)])))
#		pool.close()
#	
#	if plot:
#		for i in range(100):
#			plot_cell_at_threshold([i,electrode])
#	
#	if get_results:
##		for i in range(100):
#		pool = ThreadPool(numthreads)
#		pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[electrode for i in range(100)])))
#		pool.close()
##			plot_cell_at_fixed_amplitude([i,electrode])
#	
#	print('Finished electrode '+str(electrode))


	for diam in [10,8,6,4]:
		os.rename(os.getcwd()+'/IC_morphs_'+str(diam)+'um'+'/',os.getcwd()+'/morphs/')
		electrode = 2
		print('Starting electrode '+str(electrode))
		if estimate:
			with open(os.getcwd()+'/morphs/'+'multipro_cathodal_thresholds.txt','w') as f:
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
		
		print('Finished electrode '+str(electrode))
		os.rename(os.getcwd()+'/morphs/',os.getcwd()+'/IC_morphs_'+str(diam)+'um'+'/')
