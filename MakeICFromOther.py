import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool 
import subprocess as sp
import os
from roots.swcToolkit import swcToolkit

def load_strip_terminal(morphname):
	swctool = swcToolkit()
	tree = swctool.load(morphname)
	


if __name__ == "__main__":
	ddirs = [os.getcwd()+'/IC_morphs_'+str(i)+'um' for i in [4,6,8,10]]
	swcs = []
	for ddir in ddirs:
		swcs+=[ddir+'/'+fname for fname in os.listdir(ddir) if '.swc' in fname]
	
	
	
#	pool = ThreadPool(multiprocessing.cpu_count())
#	pool.map()
#	pool.close()
