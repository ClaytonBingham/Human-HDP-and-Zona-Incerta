import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool 
import subprocess as sp
import os


def find_cell_threshold(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_bipolar_1cathodal.py '+str(cellnum)+' '+str(electrode),shell=True)

def plot_cell_at_threshold(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_bipolar_1cathodal.py '+str(cellnum)+' '+str(electrode)+' show 0.0',shell=True)

def plot_cell_at_fixed_amplitude(topparams):
	cellnum = topparams[0]
	electrode = topparams[1]
	sp.call('python3 run_cell_estimate_threshold_bipolar_1cathodal.py '+str(cellnum)+' '+str(electrode)+' show '+str(3.0)+' fixed',shell=True)

#New
#10 - [(3,0.86),(4,0.56),(6,0.04),(7,0.28),(9,0.52),(12,0.26),(15,0.22),(18,1.52),(20,0.42),(21,1.94),(23,0.6),(24,0.64),(25,0.18),(33,0.32),(35,0.52),(36,0.3),(37,0.54),(39,0.84),(42,0.82),(44,0.04),(46,1.82),(47,1.34),(48,1.56),(49,0.74),(52,0.68),(58,0.68),(64,0.06),(65,1.08),(68,0.48),(72,1.4),(73,0.82),(74,0.62),(81,0.24),(85,0.12),(88,0.58),(93,1.74),(96,0.58)]
#8  - [(0,0.08),(3,1.2),(4,0.7),(6,0.48),(7,0.48),(9,0.66),(12,0.4),(15,0.36),(18,1.76),(20,0.62),(21,2.28),(23,0.62),(24,0.92),(25,0.36),(33,0.44),(35,0.48),(36,0.4),(37,0.62),(39,0.96),(42,1.0),(44,0.24),(46,2.08),(47,1.6),(48,1.96),(49,0.86),(52,0.8),(58,0.74),(64,0.2),(65,1.24),(68,0.54),(72,1.64),(73,1.04),(74,0.76),(81,0.4),(85,0.3),(88,0.72),(90,0.06),(93,2.26),(96,0.66)]
#6  - [(0,0.58),(3,2.1),(4,0.8),(6,0.76),(7,0.82),(9,0.92),(12,0.76),(15,0.84),(18,2.52),(19,0.12),(20,0.76),(21,3.18),(23,1.18),(24,1.5),(25,0.6),(32,0.06),(33,0.82),(35,0.6),(36,0.58),(37,0.92),(38,0.3),(39,1.26),(42,1.54),(44,0.56),(46,2.52),(47,2.24),(48,2.76),(49,1.28),(50,0.36),(52,1.2),(53,0.06),(58,1.14),(64,0.62),(65,1.64),(68,0.82),(72,2.36),(73,1.66),(74,0.98),(75,0.28),(78,0.02),(81,0.84),(85,0.56),(88,0.94),(90,0.4),(93,3.0),(96,0.86),(99,0.06)]
#4  - [(0,2.08),(1,0.74),(3,4.08),(4,2.46),(5,0.08),(6,2.48),(7,2.36),(8,0.82),(9,2.02),(12,2.14),(15,2.72),(18,5.26),(19,1.64),(20,2.12),(21,6.06),(22,0.04),(23,2.1),(24,2.6),(25,1.48),(29,0.18),(30,0.46),(31,0.74),(32,1.14),(33,2.44),(34,0.16),(35,1.36),(36,1.44),(37,2.1),(38,1.46),(39,2.34),(41,0.56),(42,2.32),(44,2.04),(46,3.88),(47,4.0),(48,4.0),(49,2.84),(50,1.94),(52,1.7),(53,0.94),(55,0.38),(57,1.2),(58,2.1),(59,0.54),(60,0.66),(62,0.86),(64,1.28),(65,3.2),(67,1.0),(68,1.98),(69,1.6),(70,1.12),(71,0.38),(72,3.62),(73,3.84),(74,2.14),(75,1.96),(76,0.6),(78,1.36),(79,0.18),(81,2.16),(83,0.36),(84,0.88),(85,1.92),(86,0.16),(87,1.3),(88,2.18),(89,0.96),(90,1.42),(93,4.5),(94,1.04),(95,0.14),(96,1.6),(97,1.26),(99,1.02)]
# - []
# - []
# - []
# - []

#Petersen
#10 - [(0,0.04),(3,0.76),(5,0.68),(16,1.3),(22,0.34),(30,1.2),(35,0.64),(42,0.66),(48,0.14),(49,0.48),(64,0.36),(70,0.40),(73,0.42),(78,0.80),(80,0.06),(95,0.64)]
#8  - [(0,0.3),(3,0.94),(5,0.78),(16,1.82),(22,0.48),(30,1.44),(35,0.78),(42,0.82),(48,0.24),(49,0.66),(64,0.6),(70,0.54),(73,0.58),(78,0.88),(80,0.28),(95,0.76)]
#6  - [(0,0.9),(3,1.2),(5,1.06),(14,0.42),(16,2.56),(22,0.7),(26,0.28),(29,0.18),(30,2.16),(34,0.08),(35,1.08),(42,1.2),(43,0.28),(44,0.12),(48,0.42),(49,0.9),(64,1.0),(70,0.84),(73,0.86),(74,0.04),(75,0.04),(77,0.3),(78,1.26),(80,0.9),(86,0.26),(91,0.12),(95,1.16),(96,0.26)]
#4  - [(0,2.0),(1,1.02),(2,1.68),(3,2.56),(4,0.12),(5,2.16),(6,1.5),(8,1.1),(9,0.96),(12,0.6),(14,1.08),(16,4.46),(20,0.34),(21,0.84),(22,1.86),(23,1.44),(25,1.92),(26,1.76),(28,1.0),(29,1.48),(30,3.42),(33,0.74),(34,1.32),(35,2.54),(36,0.82),(37,0.44),(38,0.36),(42,2.72),(43,1.3),(44,1.96),(45,0.28),(46,1.6),(48,1.28),(49,1.8),(51,0.04),(54,1.02),(56,1.28),(62,0.58),(63,0.22),(64,2.64),(67,0.44),(70,2.38),(73,1.86),(74,1.0),(75,1.5),(77,3.66),(78,2.22),(79,1.08),(80,3.08),(81,0.62),(82,0.02),(83,2.22),(85,0.72),(86,2.24),(87,0.3),(88,0.76),(90,1.02),(91,1.84),(92,0.34),(93,1.24),(95,1.66),(96,3.02),(98,0.18)]
# - []
# - []
# - []
# - []

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
#			numthreads = multiprocessing.cpu_count()
#			with open(os.getcwd()+'/morphs/'+'multipro_bipolar_thresholds_1cathodal.txt','w') as f:
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
#	#		for i in range(100):
#			pool = ThreadPool(numthreads)
#			pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[diam for i in range(100)])))
#			pool.close()
#	#			plot_cell_at_fixed_amplitude([i,electrode])
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
#			numthreads = multiprocessing.cpu_count()
#			with open(os.getcwd()+'/morphs/'+'multipro_bipolar_thresholds_1cathodal.txt','w') as f:
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
#	#		for i in range(100):
#			pool = ThreadPool(numthreads)
#			pool.map(plot_cell_at_fixed_amplitude,list(zip(range(100),[diam for i in range(100)])))
#			pool.close()
#	#			plot_cell_at_fixed_amplitude([i,electrode])
#		
#		print('Finished bipolar electrode '+str(electrode))
#		os.rename(os.getcwd()+'/morphs/',os.getcwd()+'/petersen_morphs_'+str(diam)+'um'+'/')
		
	for diam in [10,8,6,4]:
		os.rename(os.getcwd()+'/IC_morphs_'+str(diam)+'um'+'/',os.getcwd()+'/morphs/')
		electrode = 2
		print('Starting electrode '+str(electrode))
		if estimate:
			with open(os.getcwd()+'/morphs/'+'multipro_bipolar_thresholds_1cathodal.txt','w') as f:
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
