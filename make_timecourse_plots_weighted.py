import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 26})
plt.rcParams['xtick.major.size'] = 10
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 10
plt.rcParams['ytick.major.width'] = 2
import os
from sklearn.neighbors import KernelDensity as KDE

def load_sptimes_petersen(diameter,fixed_stim,contact):
	cortex = []
	terminal = []
	for cell in range(100):
		sptimes = [item for item in pd.read_csv(os.getcwd()+'/petersen_atlas/'+str(diameter)+'um_'+str(fixed_stim)+'mA/'+str(cell)+'_'+str(diameter)+'_sptimes.csv').to_dict(orient='list').values()][1:]
		cortex.append(sptimes[0])
		terminal+=sptimes[1:]
#		print('loaded cell #'+str(cell))
	return(cortex,terminal)

def load_sptimes_new(diameter,fixed_stim,contact):
	cortex = []
	terminal = []
	for cell in range(100):
		sptimes = [item for item in pd.read_csv(os.getcwd()+'/NewSynthetic/'+str(diameter)+'um_'+str(fixed_stim)+'mA/'+str(cell)+'_'+str(diameter)+'_sptimes.csv').to_dict(orient='list').values()][1:]
		cortex.append(sptimes[0])
		terminal+=sptimes[1:]
#		print('loaded cell #'+str(cell))
	return(cortex,terminal)

def load_sptimes_IC(diameter,fixed_stim,contact):
	cortex = []
	terminal = []
	for cell in range(100):
		sptimes = [item for item in pd.read_csv(os.getcwd()+'/IC/'+str(diameter)+'um_'+str(fixed_stim)+'mA/'+str(cell)+'_'+str(diameter)+'_sptimes.csv').to_dict(orient='list').values()][1:]
		cortex.append(sptimes[0])
#		terminal+=sptimes[1:]
#		print('loaded cell #'+str(cell))
	return(cortex,terminal)

def get_cortex_terminal_sps(diameter,amplitude,contact,dataset):
	if dataset=='Petersen':
		cortex,terminal = load_sptimes_petersen(diameter,amplitude,contact)
	if dataset=='Arborized':
		cortex,terminal = load_sptimes_new(diameter,amplitude,contact)
	if dataset=='IC':
		cortex,terminal = load_sptimes_IC(diameter,amplitude,contact)
	
#	print(cortex,'cortex')
	cortex = [item for item in cortex if len(item) >0]
	newcortex = []
	for item in cortex:
		newcortex+=item
	cortex = np.array(newcortex)-4
	if dataset!='IC':
		terminal = [item for item in terminal if len(item)>0]
		newterminal = []
		for item in terminal:
			newterminal+=item
		terminal = np.array(newterminal)-4
	return(cortex,terminal)

def plot_sptimes_by_stim_hist(amplitude,contact,dataset='IC'):
	diameters = [4,6,8,10]
	cortices = []
	terminals = []
	for diam in diameters:
		cortex,terminal = get_cortex_terminal_sps(diam,amplitude,contact,dataset)
		cortices.append(cortex)
		terminals.append(terminal)
	
	title_pre=dataset
	if dataset == 'IC':
		get_quad_hist(cortices[0],cortices[1],cortices[2],cortices[3],'Spike Times (ms)',title=title_pre+' Latency '+'(Bipolar)',output=title_pre+'cortices_'+str(amplitude)+'_'+str(contact)+'.png',x_lim=11,y_lim=6,dset=dataset)
	else:
		get_quad_hist(cortices[0],cortices[1],cortices[2],cortices[3],'Spike Times (ms)',title=title_pre+' HDP Latency '+'(Bipolar)',output=title_pre+'cortices_'+str(amplitude)+'_'+str(contact)+'.png',x_lim=11,y_lim=6,dset=dataset)
	if dataset!='IC':
		get_quad_hist(terminals[0],terminals[1],terminals[2],terminals[3],'Spike Times (ms)',title=title_pre+' Bouton Latency '+'(Bipolar)',output=title_pre+'terminals_'+str(amplitude)+'_'+str(contact)+'.png',x_lim=11,y_lim=3000,dset=dataset)

def get_quad_hist(one,two,three,four,key,title=None,output='test.png',x_lim=None,y_lim=None,factors=[0.6,0.25,0.1,0.05],dset='IC'):
	arborized_colors = list(reversed(['#41bcfa','#0084ff','#3700ff','#0e0170']))
	petersen_colors = list(reversed(['#ffadfa','#ff52f4','#a818a7','#5e005d']))
	ic_colors = list(reversed(['#bfbfbf','#7a7a7a','#424242','#000000']))
	if dset == 'IC':
		colors = ic_colors
	if dset=='Petersen':
		colors = petersen_colors
	if dset=='Arborized':
		colors = arborized_colors
	
	bin_edges = np.arange(0,x_lim,0.1)
	count_list = []
	binlist = []
	if 'cortices' not in output:
		factors = [item*0.5 for item in factors]
	
	counts,binn = np.histogram(four,bins=len(bin_edges),range=(bin_edges[0],bin_edges[-1]))
	binlist.append(binn)
	count_list.append(counts*factors[3])
	counts,binn = np.histogram(three,bins=len(bin_edges),range=(bin_edges[0],bin_edges[-1]))
	binlist.append(binn)
	count_list.append(counts*factors[2])
	counts,binn = np.histogram(two,bins=len(bin_edges),range=(bin_edges[0],bin_edges[-1]))
	binlist.append(binn)
	count_list.append(counts*factors[1])
	counts,binn = np.histogram(one,bins=len(bin_edges),range=(bin_edges[0],bin_edges[-1]))
	binlist.append(binn)
	count_list.append(counts*factors[0])
	labs = ['Diameter 10'+u"\u03BC"+'m','Diameter 8'+u"\u03BC"+'m','Diameter 6'+u"\u03BC"+'m','Diameter 4'+u"\u03BC"+'m']
#	plt.hist(x=[np.arange(len(li))*0.1 for li in count_list],bins = len(count_list[0]),weights=count_list,label=labs,color=['k','#67a377','#ad3e3e','#5fa1c2'],stacked=True,density=True)
	plt.hist(x=[np.arange(len(li))*0.1 for li in count_list],bins=len(count_list[0]),weights=count_list,label=labs,color=colors,stacked=True,density=False)
	plt.xlabel(key)
	if 'cortices' in output:
		plt.ylabel('Count of Cortical APs')
	else:
		plt.ylabel('Count of Bouton APs')
#	if contact == 2:
#		plt.legend()
	plt.title(title)

#	plt.grid(b=True, which='minor', color='k', linestyle='-')
#	plt.grid(b=True, which='major', color='k', linestyle='-')
	if x_lim is not None:
		plt.xlim(0,x_lim)
		plt.xticks(np.arange(0,x_lim+0.5,1.0))
	
	if y_lim is not None:
		plt.ylim(0,y_lim)
	
	fig = plt.gcf()
	fig.set_size_inches(15,9,forward=True)
	fig.savefig(output,dpi=250,bbox_inches='tight')
#	plt.show()
	plt.close('all')
#	return(count_list,binlist)

if __name__ == "__main__":
	for dataset in ['IC','Petersen','Arborized']:
		for amplitude in [3.0]:
			for contact in [2]:
				print(amplitude,contact,dataset)
				plot_sptimes_by_stim_hist(amplitude,contact,dataset)
