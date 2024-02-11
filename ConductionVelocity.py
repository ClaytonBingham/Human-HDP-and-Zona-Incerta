from neuron import h
import numpy as np
from scipy.spatial.distance import cdist
import networkx as nx
import matplotlib.pyplot as plt


class ConductionVelocity():
	def __init__(self):
		pass

	def calculateCV(self,cell,data,sectype='CCF',time_step=0.0625):
		self.cell = cell
		self.data = data #np.transpose(data)
		if sectype=='CCF':
			self.types = ['node','paranode1','paranode2','internode']
			self.region = 'Myelinated Region'
		else:
			self.types = ['bouton','interbouton']
			self.region = 'Unmyelinated Region'
		
		self.build_sections_of_interest()
		if sectype=='CCF':
			self.first_spikes = [self.calc_time_to_first_spike(self.data[i])*time_step for i in range(len(self.cell.node))]
		else:
			self.first_spikes = [self.calc_time_to_first_spike(self.data[i])*time_step for i in range(len(self.sections))]
		
		self.graph = self.build_network(self.sections)
		if self.region == 'CCF':
			self.nearest_node = self.get_node_nearest_terminal()
		else:
			self.nearest_node = np.argmin(self.first_spikes)
		
		self.path=self.get_path_from_bpoint_to_cortex()
		H = nx.subgraph(self.graph,self.path)
		nx.draw(H,with_labels=True,font_weight='bold',node_color='lightblue',node_size=500)
		plt.show()
		self.path_length = self.get_path_length(self.path)
		self.time_diff = np.abs(self.first_spikes[0]-self.first_spikes[self.nearest_node-3])
		self.mean_CV,self.std_CV = self.calculate_CV_u_sd([self.time_diff],[self.path_length])
		print('Mean (+-STD) conduction velocity of the '+self.region+' is: '+str(self.mean_CV)+'+-'+str(self.std_CV))
	
	def build_network(self,sections):
		g = nx.Graph()
		for sec in sections:
			child = h.SectionRef(sec=sec)
			if child.has_parent():
				parent = child.parent
				if parent in sections:
					g.add_edge(sections.index(parent),sections.index(sec),weight=parent.L/2.0+sec.L/2.0)
		return(g)
	
	def get_node_nearest_terminal(self,threshold=150.0):
		ib_mids = self.calc_section_midpoints(self.cell.interbouton)
		node_mids = self.calc_section_midpoints(self.cell.node)
		for node in node_mids:
			if np.min(cdist(np.array([np.array(item) for item in [node]]),np.array(ib_mids))) < threshold:
				return(node_mids.index(node))
		
		return(None)
	
	def get_path_from_bpoint_to_cortex(self):
		try:
			path = nx.dijkstra_path(self.graph,self.nearest_node,0)
			return(path)
		except:
			print('no path exists')
			return([])
	
	def get_path_length(self,path):
		testlen = 0
		for p in range(len(path[:-1])):
			testlen+=self.graph[path[p]][path[p+1]]['weight']
		return(testlen)
	
	def get_branch_point_on_ccf(self):
		ref = h.SectionRef(self.cell.internode[0])
		if ref.parent in self.sections:
			print('found branchpoint, ccf AP origin')
		return(self.sections.index(ref.parent))
	
	def calculate_CV_u_sd(self,tdiffs,distances):
		dists = np.array(distances)*1e-6 #um -> m
		times = np.array(tdiffs)*1e-3 #ms -> s
		cvs = [dists[i]/times[i] for i in range(len(dists))] #m/s
		return(np.mean(cvs),np.std(cvs))
	
	def get_spike_tdiffs(self,fspikes,chfspikes):
		return([np.abs(fspikes[i]-chfspikes[i]) for i in range(len(chfspikes)) if chfspikes is not None])
	
	def get_children_first_spikes(self,children,fspikes):
		chspikes = []
		for child in children:
			if child is None:
				chspikes.append(None)
				continue
			
			chspikes.append(fspikes[self.sections.index(child)])
		
		return(chspikes)
	
	def build_sections_of_interest(self):
		self.sections = []
		for sectype in self.types:
			if sectype == 'node':
				self.sections+=self.cell.node
			if sectype == 'paranode1':
				self.sections+=self.cell.paranode1
			if sectype == 'paranode2':
				self.sections+=self.cell.paranode2
			if sectype == 'internode':
				self.sections+=self.cell.internode
			if sectype == 'bouton':
				self.sections+=self.cell.bouton
			if sectype == 'interbouton':
				self.sections+=self.cell.interbouton
	
	def eucdist3d(self,a,b):
		return(((b[0]-a[0])**2+(b[1]-a[1])**2+(b[2]-a[2])**2)**0.5)
	
	def calc_midpoint(self,a,b):
		return([(a[0]+b[0])/2.0,(a[1]+b[1])/2.0,(a[2]+b[2])/2.0])
	
	
	def calc_time_to_first_spike(self,sec_data):
		for i in range(len(sec_data)):
			if sec_data[i] > 0.0:
				return(i)
		
		return(None)

	def calc_cell_first_spike_times(self,data):
		sptimes = []
		for section in data:
			sptimes.append(self.calc_time_to_first_spike(section))
		
		return(sptimes)

	def calc_section_midpoints(self,sections):
		midpoints = []
		for section in sections:
			if section is None:
				midpoints.append(None)
				continue
			
			section.push()
			if h.n3d() % 2 == 1:
				mid = [h.x3d(int(h.n3d()/2)), h.y3d(int(h.n3d()/2)), h.z3d(int(h.n3d()/2))]
			else:
				mid = self.calc_midpoint([h.x3d(int(h.n3d()/2)-1), h.y3d(int(h.n3d()/2)-1), h.z3d(int(h.n3d()/2)-1)],[h.x3d(int(h.n3d()/2)), h.y3d(int(h.n3d()/2)), h.z3d(int(h.n3d()/2))])
			
			midpoints.append(mid)
			h.pop_section()
		
		return(midpoints)

