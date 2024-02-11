import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})



def load_threshold(cellnum,electrode,diameter):
	dat = pd.read_csv('multipro_contact'+str(electrode)+'_thresholds_'+str(diameter)+'um.txt',names=['cell','value'],delimiter=' ',index_col=None)
	thresholds = dict(zip(dat.cell.values,dat.value.values))
	return(thresholds[cellnum])

def build_percent_active_curves(diameter):
	curves = {}
	for electrode in range(1,5):
		curves[electrode] = []
		for cellnum in range(100):
			curves[electrode].append(load_threshold(cellnum,electrode,diameter))
	
	return(curves)

def get_terms_dict_10um():
	termsdict = {}
	termsdict[1] = [1,12,21,24,28,36,49,75,93,96,99]
	termsdict[2] = [18,21,37,39,46,47,48,49,52,68,72,74,88,93,96]
	termsdict[3] = [4,9,21,25,35,36,47,48,58,74,88,96]
	termsdict[4] = [21,90,95]
	rangedict = {}
	rangedict[1] = [0.02,0.03,0.57,0.01,0.18,0.15,0.23,0.16,0.10,0.23,0.3,]
	rangedict[2] = [0.22,0.55,0.12,0.27,0.45,0.35,0.37,0.13,0.19,0.08,0.4,0.13,0.1,0.22,0.23]
	rangedict[3] = [0.12,0.01,0.56,0.17,0.13,0.03,0.44,0.19,0.26,0.24,0.22,0.22,]
	rangedict[4] = [0.12,0.05,0.11]
	return(termsdict,rangedict)
	

def get_terms_dict_8um():
	termsdict = {}
	termsdict[1] = [1,12,21,24,28,36,49,75,93,96,99]
	termsdict[2] = [18,21,37,39,46,47,48,49,52,65,68,72,74,88,93,96]
	termsdict[3] = [4,9,21,25,35,36,44,47,48,52,58,74,88,93,96]
	termsdict[4] = [19,21,58,73,90,95]
	rangedict = {}
	rangedict[1] = [0.08,0.07,0.71,0.14,0.25,0.22,0.32,0.28,0.24,0.29,0.52]
	rangedict[2] = [0.33,0.7,0.2,0.39,0.61,0.46,0.49,0.19,0.23,0.06,0.14,0.51,0.2,0.2,0.37,0.28,]
	rangedict[3] = [0.19,0.09,0.7,0.23,0.19,0.11,0.08,0.57,0.3,0.02,0.35,0.32,0.26,0.17,0.28,]
	rangedict[4] = [0.01,0.26,0.1,0.05,0.11,0.16]
	return(termsdict,rangedict)

def get_terms_dict_6um():
	termsdict = {}
	termsdict[1] = [1,12,21,24,28,36,39,49,72,75,93,96,99]
	termsdict[2] = [12,18,21,23,37,39,46,47,48,49,52,64,65,68,72,74,88,90,93,96]
	termsdict[3] = [4,9,18,21,25,35,36,39,44,47,48,52,55,58,65,72,74,88,93,96]
	termsdict[4] = [19,21,47,58,71,73,90,93,95]
	rangedict = {}
	rangedict[1] = [0.22,0.27,1.08,0.42,0.42,0.37,0.01,0.53,0.15,0.39,0.54,0.43,0.64]
	rangedict[2] = [0.09,0.67,0.98,0.09,0.4,0.56,0.89,0.75,0.67,0.4,0.33,0.12,0.35,0.3,0.71,0.37,0.35,0.06,0.71,0.44]
	rangedict[3] = [0.4,0.31,0.29,0.99,0.41,0.32,0.26,0.21,0.37,0.87,0.56,0.18,0.11,0.53,0.12,0.01,0.5,0.43,0.58,0.42]
	rangedict[4] = [0.3,0.64,0.08,0.29,0.06,0.29,0.27,0.06,0.29]
	return(termsdict,rangedict)



def count_less_than(curve,cutoff):
	count = 0
	for c in curve:
		if c<cutoff:
			count+=1
	return(count)

def sort_and_sum_curve(curve):
	xs = np.arange(np.min(curve),np.max(curve),0.02)
	ys = [count_less_than(curve,cutoff) for cutoff in xs]
	return(xs,ys)

def count_terms_active(cutoff,electrode,terms,rangedict,diameter):
	terms_first = terms[electrode]
	ranges = []
	for i in range(len(terms_first)):
		ranges.append([load_threshold(terms_first[i],electrode,diameter),load_threshold(terms_first[i],electrode,diameter)+rangedict[electrode][i]])
	
	count = 0
	for r in ranges:
		if cutoff > r[0] and cutoff < r[1]:
			count+=1
	
	return(count)

def get_proportion_terminal(terms,rangedict,curve,electrode,cutoff,diameter):
	numactive = count_less_than(curve,cutoff)
	if numactive == 0:
		return(None)
	termsactive = count_terms_active(cutoff,electrode,terms,rangedict,diameter)
	return((float(termsactive)/numactive)*100.0)



if __name__ == "__main__":
	#10um
	fig, ax1 = plt.subplots(figsize=(15,9))
	ax2 = ax1.twinx() 
	curves = build_percent_active_curves(10)
	terms,rangedict = get_terms_dict_10um()
	markers = ['.','d','v','x','o']
	for curve in curves.keys():
		if curve == 1:
			continue
		xs,ys = sort_and_sum_curve(curves[curve])
		ax1.plot(xs,ys,label='Contact '+str(curve-1),color='k',marker=markers[curve],markersize=7)
	
	ys = [[] for i in curves.keys()]
	for x in xs:
		for curve in curves.keys():
			ys[curve-1].append(get_proportion_terminal(terms,rangedict,curves[curve],curve,x,10))
	
	for curve in curves.keys():
		if curve == 1:
			continue
		ax2.plot(xs,ys[curve-1],label='Contact '+str(curve-1),color='#ad3e3e',marker=markers[curve],markersize=7)
		ax2.tick_params(axis='y',labelcolor='#ad3e3e')
	
	ax2.set_ylabel('Terminal vs. CCF Active (%)',color='#ad3e3e')
	ax1.set_xlabel('mA')
	ax1.set_xlim((0.1,1.5))
	ax1.set_ylabel('% Active')
	ax1.set_title('10um CCF')
	ax1.legend(loc='center right')
	plt.show()
	
	#8um
	fig, ax1 = plt.subplots(figsize=(15,9))
	ax2 = ax1.twinx() 
	curves = build_percent_active_curves(8)
	terms,rangedict = get_terms_dict_8um()
	markers = ['.','d','v','x','o']
	for curve in curves.keys():
		if curve == 1:
			continue
		xs,ys = sort_and_sum_curve(curves[curve])
		ax1.plot(xs,ys,label='Contact '+str(curve-1),color='k',marker=markers[curve],markersize=7)
	
	ys = [[] for i in curves.keys()]
	for x in xs:
		for curve in curves.keys():
			ys[curve-1].append(get_proportion_terminal(terms,rangedict,curves[curve],curve,x,8))
	
	for curve in curves.keys():
		if curve == 1:
			continue
		ax2.plot(xs,ys[curve-1],label='Contact '+str(curve-1),color='#ad3e3e',marker=markers[curve],markersize=7)
		ax2.tick_params(axis='y',labelcolor='#ad3e3e')
	
	ax2.set_ylabel('Terminal vs. CCF Active (%)',color='#ad3e3e')
	ax1.set_xlabel('mA')
	ax1.set_xlim((0.1,1.5))
	ax1.set_ylabel('% Active')	
	ax1.set_title('8um CCF')
	ax1.legend(loc='center right')
	plt.show()
	
	#6um
	fig, ax1 = plt.subplots(figsize=(15,9))
	ax2 = ax1.twinx() 
	curves = build_percent_active_curves(6)
	terms,rangedict = get_terms_dict_6um()
	markers = ['.','d','v','x','o']
	for curve in curves.keys():
		if curve == 1:
			continue
		xs,ys = sort_and_sum_curve(curves[curve])
		ax1.plot(xs,ys,label='Contact '+str(curve-1),color='k',marker=markers[curve],markersize=7)
	
	ys = [[] for i in curves.keys()]
	for x in xs:
		for curve in curves.keys():
			ys[curve-1].append(get_proportion_terminal(terms,rangedict,curves[curve],curve,x,6))
	
	for curve in curves.keys():
		if curve == 1:
			continue
		ax2.plot(xs,ys[curve-1],label='Contact '+str(curve-1),color='#ad3e3e',marker=markers[curve],markersize=7)
		ax2.tick_params(axis='y',labelcolor='#ad3e3e')
	
	ax2.set_ylabel('Terminal vs. CCF Active (%)',color='#ad3e3e')
	ax1.set_xlabel('mA')
	ax1.set_xlim((0.1,1.5))
	ax1.set_ylabel('% Active')
	ax1.set_title('6um CCF')
	ax1.legend(loc='center right')
	plt.show()
