import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from neuron import h
import pandas as pd
import pickle

class InterpolateField2Cell():
	def __init__(self,cellname,cellnum,cell,electrode,fieldfile='fieldsolutions.csv'): #'3389inSTN_1mAinCITspace.txt'):
		try:
			with open(os.getcwd()+'/morphs/'+str(cellnum)+'_'+str(electrode)+'_solutions.pickle','rb') as f:
				self.cell_solutions = pickle.load(f)
			with open(os.getcwd()+'/morphs/'+str(cellnum)+'_'+str(electrode)+'_centers.pickle','rb') as f:
				self.centers = pickle.load(f)
		except:
			self.fieldfile = fieldfile
			self.electrode=electrode
#			self.centers = self.get_cell_centers(cell)
			self.centers = self.load_cell_centers(cellname)
			self.field,self.solution = self.load_field()
			self.cell_solutions = [1000.0*self.interpolate_to_point(center) for center in self.centers]
			with open(os.getcwd()+'/morphs/'+str(cellnum)+'_'+str(electrode)+'_solutions.pickle','wb') as f:
				pickle.dump(self.cell_solutions,f)
			with open(os.getcwd()+'/morphs/'+str(cellnum)+'_'+str(electrode)+'_centers.pickle','wb') as f:
				pickle.dump(self.centers,f)		
		
#		self.show_distribution_of_solutions()
	
	def show_distribution_of_solutions(self):
		plt.hist(self.cell_solutions)
		plt.title('Distribution of Efield Solutions')
		plt.xlabel('Voltage (mV)')
		plt.ylabel('Count')
		plt.show()
	
	def find_nearest_four_simplices(self,point):
		dists = cdist(np.array([point]),np.array(self.field)).ravel()
		topfour = np.argsort(dists)[:4]
		return(topfour,[dists[i] for i in topfour])
	
	def interpolate_to_point(self,point):
		simplices,dists = self.find_nearest_four_simplices(point)
#		print(simplices,dists,'simpdists')
		totaldist = np.sum(dists)
		local_solutions = [self.solution[i] for i in simplices]
		return(np.sum([local_solutions[i]*(1-dists[i]/totaldist) for i in range(len(dists))]))


	def midpoint(self,a,b):
		return(((a[0]+b[0])/2.0,(a[1]+b[1])/2.0,(a[2]+b[2])/2.0))
	
	def load_cell_centers(self,cellname):
		centers = pd.read_csv(cellname)
		return(list(zip(centers.x,centers.y,centers.z)))
	
	def get_cell_centers(self,cell):
		return(self.get_section_centers(cell.all))
	
	def get_section_centers(self,sections):
		centers = []
		for section in sections:
			section.push()
			secCount = h.n3d()
			if secCount%2==1:
				centers.append(np.array([h.x3d(int(secCount/2)),h.y3d(int(secCount/2)),h.z3d(int(secCount/2))]))
			
			else:
				a = [h.x3d(int(secCount/2)),h.y3d(int(secCount/2)),h.z3d(int(secCount/2))]
				b = [h.x3d(int(secCount/2)-1),h.y3d(int(secCount/2)-1),h.z3d(int(secCount/2)-1)]
				centers.append(np.array(self.midpoint(a,b)))
			
			h.pop_section()
		
		
		return(centers)
	
	
	def load_field(self):
		dat = pd.read_csv(self.fieldfile,sep=',',names=['1','2','3','4','x','y','z'])
		points = np.array(list(zip(dat['x'],dat['y'],dat['z'])))
		solutions = np.array(dat[str(self.electrode)])
#		print('Max voltage = '+str(np.max(np.abs(solutions))))
		return(points,solutions)
