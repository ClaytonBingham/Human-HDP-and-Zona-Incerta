import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
plt.rcParams.update({'font.size': 26})
# set tick width
plt.rcParams['xtick.major.size'] = 10
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 10
plt.rcParams['ytick.major.width'] = 2

import pickle
from terms_ranges_curves import *

def get_terms_dict(diameter,waveform,dset):
	if dset == 'petersen':
		petersen_toggle=True
	else:
		petersen_toggle=False
	
	if diameter == 4:
		if waveform == 'cathodal':
			termsdict,rangedict=get_cathodal_terms_dict_4um(old=petersen_toggle)
		if waveform == 'anodal':
			termsdict,rangedict=get_anodal_terms_dict_4um(old=petersen_toggle)
		if waveform == 'bipolar':
			termsdict,rangedict=get_bipolar_terms_dict_4um(old=petersen_toggle)
	if diameter == 6:
		if waveform == 'cathodal':
			termsdict,rangedict=get_cathodal_terms_dict_6um(old=petersen_toggle)
		if waveform == 'anodal':
			termsdict,rangedict=get_anodal_terms_dict_6um(old=petersen_toggle)
		if waveform == 'bipolar':
			termsdict,rangedict=get_bipolar_terms_dict_6um(old=petersen_toggle)
	if diameter == 8:
		if waveform == 'cathodal':
			termsdict,rangedict=get_cathodal_terms_dict_8um(old=petersen_toggle)
		if waveform == 'anodal':
			termsdict,rangedict=get_anodal_terms_dict_8um(old=petersen_toggle)
		if waveform == 'bipolar':
			termsdict,rangedict=get_bipolar_terms_dict_8um(old=petersen_toggle)
	if diameter == 10:
		if waveform == 'cathodal':
			termsdict,rangedict=get_cathodal_terms_dict_10um(old=petersen_toggle)
		if waveform == 'anodal':
			termsdict,rangedict=get_anodal_terms_dict_10um(old=petersen_toggle)
		if waveform == 'bipolar':
			termsdict,rangedict=get_bipolar_terms_dict_10um(old=petersen_toggle)
	
	return(termsdict,rangedict)

def build_threshold_fname(electrode,diameter,waveform,dset):
	fname = 'multipro'
	if waveform != 'cathodal':
		fname+='_'+waveform
	else:
		fname+='_contact'+str(electrode)
	
	fname+='_thresholds'
	
	if dset != 'synthetic':
		fname+='_'+dset
	
	
	fname+='_'+str(diameter)+'um'
	fname+='.txt'
	return(os.getcwd()+'/thresholds_/'+fname)

def load_threshold_(cellnum,electrode,diameter,waveform,dset):
	dat = pd.read_csv(build_threshold_fname(electrode,diameter,waveform,dset),names=['cell','value'],delimiter=' ',index_col=None)
	thresholds = dict(zip(dat.cell.values,dat.value.values))
	return(thresholds[cellnum])

def count_less_than(curve,cutoff):
	count = 0
	for c in curve:
		if c<cutoff:
			count+=1
	return(count)

def sort_and_sum_curve(curve):
#	xs = np.arange(np.min(curve),np.max(curve),0.02)
	xs = np.arange(0.1,4.0,0.02)
	ys = [count_less_than(curve,cutoff) for cutoff in xs]
	return(xs,ys)

def sum_norm(vals,mix):
	all_None = True
	for val in vals:
		if val is not None:
			all_None = False
	
	if all_None:
		return(100.0)
	else:
		scale= 1
		for i,v in enumerate(vals):
			if v==None:
				scale-=mix[i]
		
		return(np.sum([vals[i]*mix[i]*(1/scale) for i in range(len(vals)) if vals[i] is not None]))

def sum_drop_none(lis,mix):
	e = [None for i in range(len(lis[0]))]
	for i in range(len(lis[0])):
		e[i] = sum_norm([li[i] for li in lis],mix)
	
	return(e)

def count_terms_active(cutoff,electrode,terms,rangedict,diameter,waveform,dset):
	ranges = []
	for i in range(len(terms)):
		ranges.append([load_threshold_(terms[i],electrode,diameter,waveform,dset),load_threshold_(terms[i],electrode,diameter,waveform,dset)+rangedict[i]])
	
	count = 0
	for r in ranges:
		if cutoff > r[0] and cutoff < r[1]:
			count+=1
	
	return(count)

def build_percent_active_curves(electrode,diameter,waveform,dset):
	curves = []
	for cellnum in range(100):
		try:
			curves.append(load_threshold_(cellnum,electrode,diameter,waveform,dset))
		except:
			if waveform=='bipolar':
				curves.append(4.5)
			if waveform=='anodal':
				curves.append(4.0)
#			print('cell '+str(cellnum)+' from threshold file '+build_threshold_fname(electrode,diameter,waveform,dset)+' was too high to estimate efficiently')
#			print('setting to window y-max')
	
	return(curves)

def get_threshold_curves_all(dset,waveform,electrode=1,mix=[0.05,0.1,0.25,0.6]):
	curves = []
	for i in [10,8,6,4]:
		curves.append(build_percent_active_curves(electrode,i,waveform,dset))
	
	xs = [[]]
	ys = [[]]
	x0,y0 = sort_and_sum_curve(curves[0])
	x1,y1 = sort_and_sum_curve(curves[1])
	x2,y2 = sort_and_sum_curve(curves[2])
	x3,y3 = sort_and_sum_curve(curves[3])
	xs[0] = x0
	ys[0] = np.array(y0)*mix[0]+np.array(y1)*mix[1]+np.array(y2)*mix[2]+np.array(y3)*mix[3]
	return(xs,ys)

def plot_3(waveform,electrode=1,mix=[0.05,0.1,0.25,0.6],colors = ['#fcebf4','#fcebf4','#fcebf4']):
	x0,y0 = get_threshold_curves_all('synthetic',waveform,electrode,mix)
	x1,y1 = get_threshold_curves_all('petersen',waveform,electrode,mix)
	x2,y2 = get_threshold_curves_all('IC',waveform,electrode,mix)
	fig, ax1 = plt.subplots(figsize=(15,9))
	markers = ['o','d','x']
	if waveform != 'bipolar':
		for i in range(len(x2)):
			ax1.plot(np.array(x2[i]),np.array(y2[i]),label='Internal Capsule',color=colors[0],markersize=7,linewidth=3)
		for i in range(len(x1)):
			ax1.plot(np.array(x1[i]),np.array(y1[i]),label='Petersen HDP',color=colors[2],markersize=7,linewidth=3)
		for i in range(len(x0)):
			ax1.plot(np.array(x0[i]),np.array(y0[i]),label='Arborized HDP',color=colors[1],markersize=7,linewidth=3)
	else:
		for i in range(len(x2)):
			ax1.plot(2*np.array(x2[i]),np.array(y2[i]),label='Internal Capsule',color=colors[0],markersize=7,linewidth=3)
		for i in range(len(x1)):
			ax1.plot(2*np.array(x1[i]),np.array(y1[i]),label='Petersen HDP',color=colors[2],markersize=7,linewidth=3)
		for i in range(len(x0)):
			ax1.plot(2*np.array(x0[i]),np.array(y0[i]),label='Arborized HDP',color=colors[1],markersize=7,linewidth=3)
	
	ax1.set_xlabel('mA')
	if waveform == 'bipolar':
		ax1.set_title('Activation Threshold (Bipolar)')
	if 'anod' in waveform:
		ax1.set_title('Activation Threshold (Anodic)')
	if 'cathod' in waveform:
		ax1.set_title('Activation Threshold (Cathodic)')
	
	ax1.set_ylim((-2.0,102.0))
	ax1.set_xlim((0.2,4.0))
	ax1.set_ylabel('% Active')
	if waveform =='cathodal':
		ax1.legend(loc='center right')
#	ax1.grid(linestyle='dashed',linewidth='0.5',color='k')
	plt.tight_layout()
	plt.show()
	return([x0,y0],[x1,y1])

def calculate_prop_terminals(mix,xs,electrode,waveform,dset):
	curve_ = []
	terms_ = []
	rangedict_ = []
	diams = [10,8,6,4] 
	for diam in diams:
		t,r = get_terms_dict(diam,waveform,dset)
		terms_.append(t[electrode])
		rangedict_.append(r[electrode])
		curve_.append(build_percent_active_curves(electrode,diam,waveform,dset))
	
	y0 = [get_proportion_terminal(terms_[0],rangedict_[0],curve_[0],1,x,diams[0],waveform,dset) for x in xs]
	y1 = [get_proportion_terminal(terms_[1],rangedict_[1],curve_[1],1,x,diams[1],waveform,dset) for x in xs]
	y2 = [get_proportion_terminal(terms_[2],rangedict_[2],curve_[2],1,x,diams[2],waveform,dset) for x in xs]
	y3 = [get_proportion_terminal(terms_[3],rangedict_[3],curve_[3],1,x,diams[3],waveform,dset) for x in xs]
	elec1 = sum_drop_none([y0,y1,y2,y3],mix)
	return(elec1,y0,y1,y2,y3)

def get_proportion_terminal(terms,rangedict,curve,electrode,cutoff,diameter,waveform,dset):
	numactive = count_less_than(curve,cutoff)
	if numactive == 0:
		return(None)
	termsactive = count_terms_active(cutoff,electrode,terms,rangedict,diameter,waveform,dset) #load_threshold args cellnum,electrode,diameter,waveform,dset
	return((float(termsactive)/numactive)*100.0)



def plot_prop(mix,xs,pxs,electrode,waveform,colors = ['#fcebf4','#fcebf4']):
	fig, ax1 = plt.subplots(figsize=(15,9))
	try:
		if waveform == 'bipolar':
			with open('new_bipolar_threshold_plotted_1cathodal.pickle','rb') as f:
				bsx,bsy = pickle.load(f)
			with open('petersen_bipolar_threshold_plotted_1cathodal.pickle','rb') as f:
				bpx,bpy = pickle.load(f)
		if waveform == 'anodal':
			with open('new_anodal_threshold_plotted.pickle','rb') as f:
				bsx,bsy = pickle.load(f)
			with open('petersen_anodal_threshold_plotted.pickle','rb') as f:
				bpx,bpy = pickle.load(f)
		if waveform == 'cathodal':
			with open('new_threshold_plotted_cathodal.pickle','rb') as f:
				bsx,bsy = pickle.load(f)
			with open('petersen_threshold_plotted_cathodal.pickle','rb') as f:
				bpx,bpy = pickle.load(f)
		
		if waveform=='cathodal':
			ax1.plot(bpx[2],bpy[2],label='Petersen Atlas',color=colors[1],linewidth=3)
			ax1.plot(bsx[2],bsy[2],label='New Synthetic',color=colors[0],linewidth=3)
		else:
			ax1.plot(bpx[1],bpy[1],label='Petersen Atlas',color=colors[1],linewidth=3)
			ax1.plot(bsx[1],bsy[1],label='New Synthetic',color=colors[0],linewidth=3)
	
	except:
		print('Calculating Sites of Action Potential Initiation')
		if waveform != 'bipolar':
			e1,y0,y1,y2,y3 = calculate_prop_terminals(mix,xs[0][0],electrode,waveform,dset='synthetic')
			for i,e in enumerate([e1]):
				ax1.plot([x for ii,x in enumerate(xs[0][0]) if xs[1][i][ii] != 0.0],[e[ii] for ii in range(len(e)) if xs[1][i][ii] != 0.0],label='New Synthetic Contact '+str(electrode),color='#fa58b0',linewidth=3)
			
			e1,y0,y1,y2,y3 = calculate_prop_terminals(mix,pxs[0][0],electrode,waveform,dset='petersen')
			for i,e in enumerate([e1]):
				ax1.plot([x for ii,x in enumerate(pxs[0][0]) if pxs[1][i][ii] != 0.0],[e[ii] for ii in range(len(e)) if pxs[1][i][ii] != 0.0],label='Petersen Contact '+str(electrode),color='#67a377',linewidth=3)
		else:
			e1,y0,y1,y2,y3 = calculate_prop_terminals(mix,xs[0][0],electrode,waveform,dset='synthetic')
			for i,e in enumerate([e1]):
				ax1.plot([2*x for ii,x in enumerate(xs[0][0]) if xs[1][i][ii] != 0.0],[e[ii] for ii in range(len(e)) if xs[1][i][ii] != 0.0],label='New Synthetic Contact 1-/2+',color='#fa58b0',linewidth=3)
			
			e1,y0,y1,y2,y3 = calculate_prop_terminals(mix,pxs[0][0],electrode,waveform,dset='petersen')
			for i,e in enumerate([e1]):
				ax1.plot([2*x for ii,x in enumerate(pxs[0][0]) if pxs[1][i][ii] != 0.0],[e[ii] for ii in range(len(e)) if pxs[1][i][ii] != 0.0],label='Petersen Contact 1-/2+',color='#67a377',linewidth=3)
	
	ax1.set_ylim((-2.0,102.0))
	ax1.set_xlim((0.2,4.0))
#	ax1.grid(linestyle='dashed',linewidth='0.5',color='k')
	if waveform == 'bipolar':
		ax1.set_title('Site of Action Potential Initiation (Bipolar)')
	if waveform == 'anodal':
		ax1.set_title('Site of Action Potential Initiation (Anodic)')
	if waveform == 'cathodal':
		ax1.set_title('Site of Action Potential Initiation (Cathodic)')
	
#	plt.legend()
	ax1.set_xlabel('mA')
	ax1.set_ylabel('Collateral vs. CCF (%)')
	plt.tight_layout()
	plt.show()

if __name__ == "__main__":
#	pass
	mix=[0.05,0.1,0.25,0.6]
	pcolors = ['#26292e','#FA58AF','#66B3FF']
	for waveform in ['cathodal','anodal','bipolar']:
		sxy,pxy = plot_3(waveform,1,mix,colors = [pcolors[0],pcolors[2],pcolors[1]])
		plot_prop(mix,sxy,pxy,1,waveform,colors = [pcolors[2],pcolors[1]])
