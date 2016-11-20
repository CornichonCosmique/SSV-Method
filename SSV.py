#!/usr/bin/python
# -*- coding:Utf-8 -*-

import Tkinter as tk
import tkFileDialog
import tkMessageBox
import ttk
import os, os.path
import sys
import webbrowser
import urllib

import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

from osgeo import ogr,osr,gdal
from shapely.wkb import loads
from shapely.geometry import *
from shapely.ops import *
import numpy as np
import math
import csv
from scipy import stats
import scipy



class ssvapp_tk(tk.Tk):
	def __init__(self,parent):
		tk.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		try:
			self.updateCheck()
		except IOError:
			pass

	def initialize(self):
		self.grid()
		rowI=0
		self.mainFrame = tk.Frame(self, borderwidth=2, relief="groove")
		self.mainFrame.grid(column=0, row=rowI, sticky="NSEW")
		self.mainFrame.columnconfigure(0, weight=1)
		self.mainFrame.columnconfigure(1, weight=1)
		self.mainFrame.columnconfigure(2, weight=1)
		self.mainFrame.columnconfigure(3, weight=1)
		self.mainFrame.columnconfigure(4, weight=1)
		self.mainFrame.columnconfigure(5, weight=1)
		self.mainFrame.columnconfigure(6, weight=1)
		self.mainFrame.columnconfigure(7, weight=1)
		self.mainFrame.columnconfigure(8, weight=1)
		
		#row 1
		rowI=rowI+1
		helpLabel = tk.Label(self.mainFrame, text="Help and tutorial", fg="blue", cursor="hand2",anchor="sw")
		helpLabel.grid(column=0,row=rowI, sticky="W")
		helpLabel.bind("<Button-1>", self.openHelp)
		
		self.extractButton = tk.Button(self.mainFrame, text="Contour lines\nextraction", command=self.contourWindow)
		self.extractButton.grid(column=1,row=rowI, sticky="W")
		
		#row 2
		rowI=rowI+1
		videLabel1 = tk.Label(self.mainFrame)
		videLabel1.grid(column=0, row=rowI, sticky="EW")
		
		#row 3
		rowI=rowI+1
		self.inputLabel = tk.Label(self.mainFrame, text="Input datas")
		self.inputLabel.grid(column=0, columnspan=4, row=rowI, sticky="EW")
		
		videmidLabel = tk.Label(self.mainFrame, width=5)
		videmidLabel.grid(column=4, row=rowI, sticky="EW")
		
		graphLabel = tk.Label(self.mainFrame, text="Graphic parameters")
		graphLabel.grid(column=5, columnspan=3, row=rowI, sticky="EW")
		
		#row 4
		rowI=rowI+1
		self.DEMLabel = tk.Label(self.mainFrame, text="DEM")
		self.DEMLabel.grid(column=0, row=rowI, sticky="EW")
		self.DEMFile = tk.StringVar()
		self.DEMFile.set("")
		self.DEMEntry = tk.Entry(self.mainFrame, width=50, textvariable=self.DEMFile)
		self.DEMEntry.grid(column=1, columnspan=2, row=rowI, sticky="EW")
		self.DEMButton = tk.Button(self.mainFrame, text="Open", command=lambda: self.open_file(self.DEMFile))
		self.DEMButton.grid(column=3, row=rowI, sticky="NSEW")
		
		self.hist2dresLabel = tk.Label(self.mainFrame, text="Number of hexagone\nalong x-axis in 2D histogramm")
		self.hist2dresLabel.grid(column=5, row=rowI, sticky="EW")
		self.hist2dres = tk.IntVar()
		self.hist2dres.set(100)
		self.hist2dresEntry = tk.Entry(self.mainFrame, width=10, textvariable=self.hist2dres,justify="right")
		self.hist2dresEntry.grid(column=6, row=rowI, sticky="E")
		
		#row 5
		rowI=rowI+1
		self.faultLabel = tk.Label(self.mainFrame, text="Fault shapefile")
		self.faultLabel.grid(column=0, row=rowI, sticky="EW")
		self.faultShapefile = tk.StringVar()
		self.faultShapefile.set("")
		self.faultEntry = tk.Entry(self.mainFrame, width=50, textvariable=self.faultShapefile)
		self.faultEntry.grid(column=1, columnspan=2, row=rowI, sticky="EW")
		self.faultButton = tk.Button(self.mainFrame, text="Open", command=lambda: self.open_file(self.faultShapefile))
		self.faultButton.grid(column=3, row=rowI, sticky="NSEW")
		
		self.histlatLabel = tk.Label(self.mainFrame, text="Bin size of\nlateral offset histogram")
		self.histlatLabel.grid(column=5, row=rowI, sticky="EW")
		self.histlat = tk.IntVar()
		self.histlat.set(10)
		self.histlatEntry = tk.Entry(self.mainFrame, width=10, textvariable=self.histlat,justify="right")
		self.histlatEntry.grid(column=6, row=rowI, sticky="E")
		self.histlatunitLabel = tk.Label(self.mainFrame, text="	 meter(s)")
		self.histlatunitLabel.grid(column=7, row=rowI, sticky="W")
		
		#row 6
		rowI=rowI+1
		self.contourLabel = tk.Label(self.mainFrame, text="Contour lines\nshapefile")
		self.contourLabel.grid(column=0, row=rowI, sticky="EW")
		self.contourShapefile = tk.StringVar()
		self.contourShapefile.set("")
		self.contourEntry = tk.Entry(self.mainFrame, width=50, textvariable=self.contourShapefile)
		self.contourEntry.grid(column=1, columnspan=2, row=rowI, sticky="EW")
		self.contourButton = tk.Button(self.mainFrame, text="Open", command=lambda: self.open_file(self.contourShapefile))
		self.contourButton.grid(column=3, row=rowI, sticky="NSEW")
		
		self.histvertLabel = tk.Label(self.mainFrame, text="Bin size of\nvertical offset histogram")
		self.histvertLabel.grid(column=5, row=rowI, sticky="EW")
		self.histvert = tk.IntVar()
		self.histvert.set(10)
		self.histvertEntry = tk.Entry(self.mainFrame, width=10, textvariable=self.histvert,justify="right")
		self.histvertEntry.grid(column=6, row=rowI, sticky="E")
		self.histvertunitLabel = tk.Label(self.mainFrame, text="	 meter(s)")
		self.histvertunitLabel.grid(column=7, row=rowI, sticky="W")
		
		#row 7
		rowI=rowI+1
		self.confidenceLabel = tk.Label(self.mainFrame, text="Excluded area(s)\nshapefile")
		self.confidenceLabel.grid(column=0, row=rowI, sticky="EW")
		self.confidenceShapefile = tk.StringVar()
		self.confidenceShapefile.set("")
		self.confidenceEntry = tk.Entry(self.mainFrame, width=50, textvariable=self.confidenceShapefile)
		self.confidenceEntry.grid(column=1, columnspan=2, row=rowI, sticky="EW")
		self.confidenceButton = tk.Button(self.mainFrame, text="Open", command=lambda: self.open_file(self.confidenceShapefile))
		self.confidenceButton.grid(column=3, row=rowI, sticky="NSEW")
		
		#row 8
		rowI=rowI+1
		self.distanceLabel = tk.Label(self.mainFrame, text="Distance max\nfrom fault")
		self.distanceLabel.grid(column=0, row=rowI, sticky="EW")
		self.distance = tk.DoubleVar()
		self.distance.set(50.0)
		self.distanceEntry = tk.Entry(self.mainFrame, justify="right", width=10, textvariable=self.distance)
		self.distanceEntry.grid(column=1,row=rowI, sticky="E")
		self.distanceunitLabel = tk.Label(self.mainFrame, text="	 meter(s)")
		self.distanceunitLabel.grid(column=2, row=rowI, sticky="W")
		
		self.redrawButton = tk.Button(self.mainFrame, text="Redraw graphic", state = 'disabled',command=lambda : self.draw_fig(self.a,self.b,self.lateral_offset,self.vertical_offset,self.figsave.get(),self.hist2dres.get(),self.histlat.get(),self.histvert.get()) )
		self.redrawButton.grid(column=5,columnspan=3, row=rowI)
		
		#row 9
		rowI=rowI+1
		videLabel2 = tk.Label(self.mainFrame)
		videLabel2.grid(column=0, row=rowI, sticky="EW")
		
		#row 10
		rowI=rowI+1
		inputLabel = tk.Label(self.mainFrame, text="Outputs")
		inputLabel.grid(column=0, columnspan=4, row=rowI, sticky="EW")
		
		#row 10 -> 23
		self.rowgraph=rowI
		self.fig = plt.figure(figsize=(6,6))
		self.canvas = FigureCanvasTkAgg(self.fig,master=self.mainFrame)
		axes = self.fig.add_subplot(111)
		axes.axis([0,10,0,10])
		axes.get_xaxis().set_ticks([])
		axes.get_yaxis().set_ticks([])
 		axes.text(5,5,"A nice looking figure\nwill appear here.",ha='center',fontsize=18)
 		plt.close('all')
 		self.canvas._tkcanvas.grid(column=5, row=rowI, rowspan=13, columnspan=3, sticky="EW")
 		
		#row 11
		rowI=rowI+1
		self.offsetsaveLabel = tk.Label(self.mainFrame, text="Offset measurements\nbackup CSV file")
		self.offsetsaveLabel.grid(column=0, row=rowI, sticky="EW")
		self.offsetSave = tk.StringVar()
		self.offsetSave.set("")
		self.offsetsaveEntry = tk.Entry(self.mainFrame, textvariable=self.offsetSave)
		self.offsetsaveEntry.grid(column=1, columnspan=2, row=rowI, sticky="EW")
		self.offsetsaveButton = tk.Button(self.mainFrame, text="Select", command=lambda: self.save_file(self.offsetSave,".csv"))
		self.offsetsaveButton.grid(column=3, row=rowI, sticky="NSEW")
		
		#row 12
		rowI=rowI+1
		self.figsaveLabel = tk.Label(self.mainFrame, text="Figure output file")
		self.figsaveLabel.grid(column=0, row=rowI, sticky="EW")
		self.figsave = tk.StringVar()
		self.figsave.set("")
		self.figsaveEntry = tk.Entry(self.mainFrame, textvariable=self.figsave)
		self.figsaveEntry.grid(column=1, columnspan=2, row=rowI, sticky="EW")
		self.figsaveButton = tk.Button(self.mainFrame, text="Select", command=lambda: self.save_file(self.figsave,".svg"))
		self.figsaveButton.grid(column=3, row=rowI, sticky="NSEW")
		
		#row 13
		rowI=rowI+1
		videLabel4 = tk.Label(self.mainFrame)
		videLabel4.grid(column=0, row=rowI, sticky="EW")
				
		#row 14
		rowI=rowI+1
		self.check = tk.IntVar()
		self.offsetCheckbox = tk.Checkbutton(self.mainFrame, text="Use offsets measurement file",variable=self.check,command=lambda v=self.check: self.test_chekbutton_pos(v))
		self.offsetCheckbox.grid(column=0, columnspan=4, row=rowI, sticky="EW")
		
		#row 15
		rowI=rowI+1
		self.offsetLabel = tk.Label(self.mainFrame, text="Offsets measurement\nCSV file",state='disabled')
		self.offsetLabel.grid(column=0, row=rowI, sticky="EW")
		self.offsetCSV = tk.StringVar()
		self.offsetCSV.set("")
		self.offsetEntry = tk.Entry(self.mainFrame, width=50, textvariable=self.offsetCSV,state='disabled')
		self.offsetEntry.grid(column=1, columnspan=2, row=rowI, sticky="EW")
		self.offsetButton = tk.Button(self.mainFrame, text="Open", command=lambda: self.open_file(self.offsetCSV),state='disabled')
		self.offsetButton.grid(column=3, row=rowI, sticky="NSEW")
		
		#row 16
		rowI=rowI+1
		videLabel6 = tk.Label(self.mainFrame)
		videLabel6.grid(column=0, row=rowI, sticky="EW")
				
		#row 17
		rowI=rowI+1
		computeLabel = tk.Label(self.mainFrame, text="Compute parameters")
		computeLabel.grid(column=0, columnspan=4, row=rowI, sticky="EW")
		
		#row 18
		rowI=rowI+1
		self.outliersLabel = tk.Label(self.mainFrame, text="Remove outliers")
		self.outliersLabel.grid(column=0, row=rowI, sticky="EW")
		self.outliers = tk.DoubleVar()
		self.outliers.set(0.99)
		self.outliersEntry = tk.Entry(self.mainFrame, width=10, textvariable=self.outliers,justify="right")
		self.outliersEntry.grid(column=1, row=rowI, sticky="E")
		self.outlierslimLabel = tk.Label(self.mainFrame, text="	 Between 0-1")
		self.outlierslimLabel.grid(column=2, row=rowI, sticky="W")
		
		#row 19
		rowI=rowI+1
		self.meanconfLabel = tk.Label(self.mainFrame, text="Confidence level of the standard\nerror of the mean offset")
		self.meanconfLabel.grid(column=0, row=rowI, sticky="EW")
		self.meanconf = tk.DoubleVar()
		self.meanconf.set(0.95)
		self.meanconfEntry = tk.Entry(self.mainFrame, width=10, textvariable=self.meanconf,justify="right")
		self.meanconfEntry.grid(column=1, row=rowI, sticky="E")
		self.meanconflimLabel = tk.Label(self.mainFrame, text="	 Between 0-1")
		self.meanconflimLabel.grid(column=2, row=rowI, sticky="W")
		
		#row 20
		rowI=rowI+1
		videLabel8 = tk.Label(self.mainFrame)
		videLabel8.grid(column=0, row=rowI, sticky="EW")
		
		
		#row 21
		rowI=rowI+1
		self.computeButton = tk.Button(self.mainFrame, text="Compute fault offset", command=self.launch)
		self.computeButton.grid(column=0, row=rowI)
		
		self.progressLabel= tk.Label(self.mainFrame, text="Progress",state='disabled')
		self.progressLabel.grid(column=1, row=rowI)
		
		self.progressbar = ttk.Progressbar(self.mainFrame, orient='horizontal', mode='determinate', value = 0)
		self.progressbar.grid(column=2,columnspan=2, row=rowI,sticky="EW")
		
		#row 22
		rowI=rowI+1
		videLabel9 = tk.Label(self.mainFrame)
		videLabel9.grid(column=0, row=rowI, sticky="EW")
		self.lateralResultLabel = tk.Label(self.mainFrame, text="Lateral offset",state='disabled')
		self.lateralResultLabel.grid(column=1, row=rowI, sticky="S")
		self.verticalResultLabel = tk.Label(self.mainFrame, text="Vertical offset",state='disabled')
		self.verticalResultLabel.grid(column=2, row=rowI, sticky="S")
		
		#row 23
		rowI=rowI+1
		self.resultLabel = tk.Label(self.mainFrame, text="Result",state='disabled')
		self.resultLabel.grid(column=0, row=rowI, sticky="E")
		self.lateralResult = tk.StringVar()
		self.lateralResult.set("")
		self.lateralResultEntry = tk.Entry(self.mainFrame, textvariable=self.lateralResult,state='disabled',justify='center')
		self.lateralResultEntry.grid(column=1, row=rowI)
		
		self.verticalResult = tk.StringVar()
		self.verticalResult.set("")
		self.verticalResultEntry = tk.Entry(self.mainFrame, textvariable=self.verticalResult,state='disabled',justify='center')
		self.verticalResultEntry.grid(column=2, row=rowI)
		
		#row 24
		rowI=rowI+1
		videLabel27 = tk.Label(self.mainFrame, text="©0|)é 3|\| 5£!|* ©|-|4|_|5537735", anchor="se")
		videLabel27.grid(column=0, columnspan=9, row=rowI, sticky="EW")
		
		
		
 	def test_chekbutton_pos(self,var):
		if var.get() == 1:
			self.offsetLabel.config(state='normal')
			self.offsetEntry.config(state='normal')
			self.offsetButton.config(state='normal')
			self.inputLabel.config(state='disabled')
			self.inputLabel.config(state='disabled')
			self.inputLabel.config(state='disabled')
			self.DEMLabel.config(state='disabled')
			self.DEMEntry.config(state='disabled')
			self.DEMButton.config(state='disabled')
			self.faultLabel.config(state='disabled')
			self.faultEntry.config(state='disabled')
			self.faultButton.config(state='disabled')
			self.contourLabel.config(state='disabled')
			self.contourEntry.config(state='disabled')
			self.contourButton.config(state='disabled')
			self.confidenceLabel.config(state='disabled')
			self.confidenceEntry.config(state='disabled')
			self.confidenceButton.config(state='disabled')
			self.distanceLabel.config(state='disabled')
			self.distanceEntry.config(state='disabled')
			self.distanceunitLabel.config(state='disabled')
			self.offsetsaveLabel.config(state='disabled')
			self.offsetsaveEntry.config(state='disabled')
			self.offsetsaveButton.config(state='disabled')
		else:
			self.offsetLabel.config(state='disabled')
			self.offsetEntry.config(state='disabled')
			self.offsetButton.config(state='disabled')
			self.inputLabel.config(state='normal')
			self.inputLabel.config(state='normal')
			self.inputLabel.config(state='normal')
			self.DEMLabel.config(state='normal')
			self.DEMEntry.config(state='normal')
			self.DEMButton.config(state='normal')
			self.faultLabel.config(state='normal')
			self.faultEntry.config(state='normal')
			self.faultButton.config(state='normal')
			self.contourLabel.config(state='normal')
			self.contourEntry.config(state='normal')
			self.contourButton.config(state='normal')
			self.confidenceLabel.config(state='normal')
			self.confidenceEntry.config(state='normal')
			self.confidenceButton.config(state='normal')
			self.distanceLabel.config(state='normal')
			self.distanceEntry.config(state='normal')
			self.distanceunitLabel.config(state='normal')
			self.offsetsaveLabel.config(state='normal')
			self.offsetsaveEntry.config(state='normal')
			self.offsetsaveButton.config(state='normal')
	
	def openHelp(self,event):
		webbrowser.open_new(r"http://geolgis.wordpress.com/2016/08/02/ssv-method/")
	
	#from http://stackoverflow.com/questions/12842693/python-check-for-updates-for-a-program
	def updateCheck(self):
		#Gets downloaded version
		self.versionSource = "1.0"
		#gets newest version
		self.updateSource = urllib.urlopen("https://raw.githubusercontent.com/CornichonCosmique/SSV-Method/master/version.txt")
		self.updateContents = self.updateSource.read()
		#checks for updates
		for i in range(0,3):
			if self.versionSource[i] != self.updateContents[i]:
				tkMessageBox.showinfo("","New version available.\nFind it following the \"Help and tutorial\" link.")
				break
	
	def contourWindow(self):
		self.extractButton.configure(state='disabled')
		self.windowCountour = tk.Toplevel(self)
		self.windowCountour.wm_attributes("-topmost", 1)
		self.windowCountour.focus_force()
		self.windowCountour.title("Contour lines extraction")
		self.windowCountour.grid()
		rowICountour=0
		self.mainFrameCountour = tk.Frame(self.windowCountour, borderwidth=2, relief="groove")
		self.mainFrameCountour.grid(column=0, row=rowICountour, sticky="NSEW")
		self.mainFrameCountour.columnconfigure(0, weight=1)
		self.mainFrameCountour.columnconfigure(1, weight=1)
		self.mainFrameCountour.columnconfigure(2, weight=1)
		
		rowICountour=rowICountour+1
		videLabelC1 = tk.Label(self.mainFrameCountour)
		videLabelC1.grid(column=0, row=rowICountour, sticky="EW")
		
		rowICountour=rowICountour+1
		inputLabelC = tk.Label(self.mainFrameCountour, text="Input datas")
		inputLabelC.grid(column=0, columnspan=3, row=rowICountour, sticky="EW")
		
		rowICountour=rowICountour+1
		self.DEMLabelC = tk.Label(self.mainFrameCountour, text="DEM")
		self.DEMLabelC.grid(column=0, row=rowICountour, sticky="EW")
		self.DEMFileC = tk.StringVar()
		self.DEMFileC.set("")
		self.DEMEntryC = tk.Entry(self.mainFrameCountour, width=50, textvariable=self.DEMFileC)
		self.DEMEntryC.grid(column=1, row=rowICountour, sticky="EW")
		self.DEMButtonC = tk.Button(self.mainFrameCountour, text="Open", command=lambda: self.open_file(self.DEMFileC))
		self.DEMButtonC.grid(column=2, row=rowICountour, sticky="NSEW")
		
		rowICountour=rowICountour+1
		self.faultLabelC = tk.Label(self.mainFrameCountour, text="Fault shapefile")
		self.faultLabelC.grid(column=0, row=rowICountour, sticky="EW")
		self.faultShapefileC = tk.StringVar()
		self.faultShapefileC.set("")
		self.faultEntryC = tk.Entry(self.mainFrameCountour, width=50, textvariable=self.faultShapefileC)
		self.faultEntryC.grid(column=1, columnspan=2, row=rowICountour, sticky="EW")
		self.faultButtonC = tk.Button(self.mainFrameCountour, text="Open", command=lambda: self.open_file(self.faultShapefileC))
		self.faultButtonC.grid(column=2, row=rowICountour, sticky="NSEW")
		
		rowICountour=rowICountour+1
		videLabelC2 = tk.Label(self.mainFrameCountour)
		videLabelC2.grid(column=0, row=rowICountour, sticky="EW")
		rowICountour=rowICountour+1
		videLabelC3 = tk.Label(self.mainFrameCountour)
		videLabelC3.grid(column=0, row=rowICountour, sticky="EW")
		
		rowICountour=rowICountour+1
		outputLabelC = tk.Label(self.mainFrameCountour, text="Output")
		outputLabelC.grid(column=0, columnspan=3, row=rowICountour, sticky="EW")
				
		rowICountour=rowICountour+1
		self.shpsaveLabel = tk.Label(self.mainFrameCountour, text="Output shapefile")
		self.shpsaveLabel.grid(column=0, row=rowICountour, sticky="EW")
		self.shpsave = tk.StringVar()
		self.shpsave.set("")
		self.shpsaveEntry = tk.Entry(self.mainFrameCountour, textvariable=self.shpsave)
		self.shpsaveEntry.grid(column=1, columnspan=2, row=rowICountour, sticky="EW")
		self.shpsaveButton = tk.Button(self.mainFrameCountour, text="Select", command=lambda: self.save_file(shpsave,".shp"))
		self.shpsaveButton.grid(column=2, row=rowICountour, sticky="NSEW")
		
		rowICountour=rowICountour+1
		videLabelC4 = tk.Label(self.mainFrameCountour)
		videLabelC4.grid(column=0, row=rowICountour, sticky="EW")
		rowICountour=rowICountour+1
		videLabelC5 = tk.Label(self.mainFrameCountour)
		videLabelC5.grid(column=0, row=rowICountour, sticky="EW")
		
		rowICountour=rowICountour+1
		self.computeButtonC = tk.Button(self.mainFrameCountour, text="Extract contour levels", command=lambda: self.extract_contour_lines(self.faultShapefileC.get(),self.DEMFileC.get(),self.shpsave.get()))
		self.computeButtonC.grid(column=1, row=rowICountour)
		
		rowICountour=rowICountour+1
		videLabelC6 = tk.Label(self.mainFrameCountour)
		videLabelC6.grid(column=0, row=rowICountour, sticky="EW")
		
		def quit_win():
			self.windowCountour.destroy()
			self.extractButton.configure(state='normal')
		self.windowCountour.protocol("WM_DELETE_WINDOW", quit_win) 
		
	def erreur(self,text) :
		tkMessageBox.showerror("Error", text)
	
	def open_file(self,fichier) :
		rep = os.path.dirname(sys.argv[0])
		fic = ""
		repfic = tkFileDialog.askopenfilename(title="Open file:", initialdir=rep,initialfile=fic, filetypes = [("All", "*"),("Shapefile","*.shp")]) 
		if len(repfic) > 0:
			rep=os.path.dirname(repfic)
			fic=os.path.basename(repfic)
		fichier.set(repfic)
	
	def save_file(self,fichier,extension) :
		rep = os.path.dirname(sys.argv[0])
		fic = ""
		repfic = tkFileDialog.asksaveasfilename(title="Save file:", initialdir=rep, defaultextension=extension)
		if len(repfic) > 0:
			rep=os.path.dirname(repfic)
			fic=os.path.basename(repfic)
		fichier.set(repfic)
			
	#extract point value from raster
	#from http://www.portailsig.org/content/python-utilisation-des-couches-vectorielles-et-matricielles-dans-une-perspective-geologique-
	def Val_raster(self,xp,yp,layer,bands,gt) :
		value=[]
		px = int((xp - gt[0]) / gt[1])
		py = int((yp - gt[3]) / gt[5])
		for j in range(bands):
			band = layer.GetRasterBand(j+1)
			data = band.ReadAsArray(px,py, 1, 1)
			value.append(data[0][0])
		return value
		
	#Iterate over pairs in a list and return pair of points
	def pair(self,list):
		for n in range(1, len(list)):
			yield list[n-1], list[n]
	
	#range with float
	def drange(self,start, stop, step):
		r = start
		while r < stop:
			yield r
			r += step
			
	#cut a curved line by another and return the two longest
	def cut(self,line, another_line):
		cut_tmp = cascaded_union([line, another_line])
		list_cut_coords=[]
		line_lenght=[]
		out=[]
		for l in cut_tmp.geoms:
			list_cut_coords.append(LineString(l.coords))
		for coords in list_cut_coords:
			line_lenght.append(len(coords.coords))
		while len(out)!=2:
			out.append(list_cut_coords[line_lenght.index(max(line_lenght))])
			list_cut_coords.pop(line_lenght.index(max(line_lenght)))
			line_lenght.pop(line_lenght.index(max(line_lenght)))
		return out
	
	#contour lines extraction
	def extract_contour_lines(self,fault_shapefile,DEM,output_shapefile):
		##### read fault shapefile
		fault = ogr.Geometry(ogr.wkbLineString)
		src_fault = ogr.Open(fault_shapefile)	
		lyr_fault = src_fault.GetLayer()
		###### read elevation raster
		couche = gdal.Open(DEM)
		gt = couche.GetGeoTransform()
		bandes = couche.RasterCount
		
		increment = math.sqrt(gt[1]**2+gt[5]**2)
		list_z = ""
		
		for elementf in lyr_fault:
			geomf = elementf.GetGeometryRef()
			fault_shp = loads(geomf.ExportToWkb())
			for seg_start, seg_end in self.pair(fault_shp.coords):
				line_start = Point(seg_start)
				line_end = Point(seg_end)
				segment = LineString([line_start.coords[0],line_end.coords[0]])
				for distance_along_fault in self.drange(0,segment.length,increment):
					point = segment.interpolate(distance_along_fault)
					list_z = list_z+str(self.Val_raster(point.x,point.y,couche,bandes,gt)[0])+" "
		os.system("gdal_contour -a z -fl "+list_z+DEM+" "+output_shapefile)
	
	
		
	#perform apparent offset measurements
	def apparent_offset_measurements(self,fault_shapefile,confidence_shapefile,DEM,contour_shapefile,distancefmax=None):
		if distancefmax is None:
			distancefmax = 50
		##### read fault shapefile
		fault = ogr.Geometry(ogr.wkbLineString)
		src_fault = ogr.Open(fault_shapefile)	
		lyr_fault = src_fault.GetLayer()
		fault_segments_lst = []
		for elementf in lyr_fault:
			geomf = elementf.GetGeometryRef()
			fault_shp = loads(geomf.ExportToWkb())
			for seg_start, seg_end in self.pair(fault_shp.coords): #for each linear fault segment	
				line_start = Point(seg_start)
				line_end = Point(seg_end)
				fault_segments_lst.append(LineString([line_start.coords[0],line_end.coords[0]]))
		self.fault_segment_number = float(len(fault_segments_lst))
		##### read confidence shapefile
		confidence = ogr.Geometry(ogr.wkbLineString)
		src_confidence = ogr.Open(confidence_shapefile)	
		lyr_confidence = src_confidence.GetLayer()
		for poly in lyr_confidence:
			geom = poly.GetGeometryRef()
			confidence = confidence.Union(geom)
		confidence_shp = loads(confidence.ExportToWkb())
		##### read contour lines shapefile
		contours = ogr.Geometry(ogr.wkbLineString)
		src_contours = ogr.Open(contour_shapefile)	
		lyr_contours = src_contours.GetLayer()
		contours_lst = []
		for contour in lyr_contours:
			geom_contour = contour.GetGeometryRef()
			contours_lst.append(loads(geom_contour.ExportToWkb()))
		self.contour_number = float(len(contours_lst))
		###### read elevation raster
		couche = gdal.Open(DEM)
		#get parameters of the raster
		gt = couche.GetGeoTransform()
		bands = couche.RasterCount 
		#start apparent offset measurements
		vect_possible_x_z= []
		increment = math.sqrt(gt[1]**2+gt[5]**2)
		
		for segment in fault_segments_lst:
				line_start = Point(segment.coords[0])
				#creation of parallel segment on both sides of the fault segment
				segment_paral2 = segment.parallel_offset(distancefmax,'left')
				segment_paral1_tmp = segment.parallel_offset(distancefmax,'right')		
				segment_paral1 = LineString([segment_paral1_tmp.coords[1],segment_paral1_tmp.coords[0]])
				segment_paral3_tmp = segment.parallel_offset(1,'right')
				segment_paral3 = LineString([segment_paral3_tmp.coords[1],segment_paral3_tmp.coords[0]])
				#creation of a boxe on the right side of the fault segment
				right_side=Polygon([segment_paral3.coords[0],segment_paral3.coords[1],segment_paral1_tmp.coords[0],segment_paral1_tmp.coords[1]])
				for contour_shp in contours_lst:
					self.progressbar.step((100/(self.fault_segment_number*self.contour_number)))
					self.progressbar.update_idletasks()
					if contour_shp.intersects(segment):
						#cut the contour line in two
						contour_split = MultiLineString(self.cut(contour_shp, segment))
						# test of possible errors
						if len(contour_split) > 2:
							print "Bug: more than two semi-contour line. Pass to the next contour line."
						elif len(contour_split) < 2:
							print "Bug: less than two semi-contour line. Pass to the next contour line."
						else :
							if contour_split[0].intersects(right_side) and contour_split[1].intersects(right_side):
								print "Bug: both semi-contour lines are on the right side. Pass to the next contour line."
							elif contour_split[0].disjoint(right_side) and contour_split[1].disjoint(right_side):
								print "Bug: both semi-contour lines are on the left side. Pass to the next contour line."
							else:
								x_all_contour_right_side,x_contour_right_side,y_contour_right_side = [], [], []
								x_all_contour_left_side,x_contour_left_side,y_contour_left_side = [], [], []
								for semi_contour in contour_split:
									#extraction of the nodes of the semi-contour line
									if semi_contour.intersects(right_side):
										for coords_contour_right_side in semi_contour.coords :
											point = Point(coords_contour_right_side)
											x_all_contour_right_side.append(point.x)
											if not point.within(confidence_shp):
												x_contour_right_side.append(point.x)
												y_contour_right_side.append(point.y)
									else:
										for coords_contour_left_side in semi_contour.coords :
											point = Point(coords_contour_left_side)
											x_all_contour_left_side.append(point.x)
											if not point.within(confidence_shp):
												x_contour_left_side.append(point.x)
												y_contour_left_side.append(point.y)
								if len(x_contour_right_side)>1 and len(x_contour_left_side)>1:
									#calculation of regression lines for the contour lines
									contour_right_side_reg_a = stats.linregress(x_contour_right_side,y_contour_right_side)[0]
									contour_right_side_reg_b = stats.linregress(x_contour_right_side,y_contour_right_side)[1]
									contour_left_side_reg_a = stats.linregress(x_contour_left_side,y_contour_left_side)[0]
									contour_left_side_reg_b = stats.linregress(x_contour_left_side,y_contour_left_side)[1]
									tendance_contour_right_side = LineString([(min(x_all_contour_right_side)-10**9,contour_right_side_reg_a*(min(x_all_contour_right_side)-10**9)+contour_right_side_reg_b),(max(x_all_contour_right_side)+10**9,contour_right_side_reg_a*(max(x_all_contour_right_side)+10**9)+contour_right_side_reg_b)])
									tendance_contour_left_side = LineString([(min(x_all_contour_left_side)-10**9,contour_left_side_reg_a*(min(x_all_contour_left_side)-10**9)+contour_left_side_reg_b),(max(x_all_contour_left_side)+10**9,contour_left_side_reg_a*(max(x_all_contour_left_side)+10**9)+contour_left_side_reg_b)])
									#test if regression lines of the contour lines intersect the fault
									if tendance_contour_right_side.intersects(segment) and tendance_contour_left_side.intersects(segment):
										offset_point = tendance_contour_left_side.intersection(segment)
										pt2 = tendance_contour_right_side.intersection(segment)
										#creation of the topographic profiles
										boundary_right_topo_profil = segment_paral1.interpolate(line_start.distance(offset_point))
										boundary_left_topo_profil = segment_paral2.interpolate(line_start.distance(offset_point))
										right_topo_profil = LineString([offset_point,boundary_right_topo_profil])
										left_topo_profil = LineString([offset_point,boundary_left_topo_profil])
										dist_from_fault_right = []
										z_right = []
										for distance_along_profil_droit in  np.arange(0,right_topo_profil.length,increment):
											point = right_topo_profil.interpolate(distance_along_profil_droit)
											if not point.within(confidence_shp):									
												dist_from_fault_right.append(distance_along_profil_droit)
												z_right.append(self.Val_raster(point.x,point.y,couche,bands,gt)[0])
										dist_from_fault_left = []
										z_left = []							
										for distance_along_profil_gauche in np.arange(0,left_topo_profil.length,increment):
											point = left_topo_profil.interpolate(distance_along_profil_gauche)								
											if not point.within(confidence_shp):									
												dist_from_fault_left.append(distance_along_profil_gauche)
												z_left.append(self.Val_raster(point.x,point.y,couche,bands,gt)[0])
										if len(z_right)>1 and len(z_left)>1:
											b_right_profil = stats.linregress(dist_from_fault_right,z_right)[1]
											b_left_profil = stats.linregress(dist_from_fault_left,z_left)[1]
											#apparent offset measurements
											vect_possible_x_z.append((line_start.distance(offset_point)-line_start.distance(pt2),b_right_profil-b_left_profil))
		return vect_possible_x_z
	
	#save apparent offset measurements in a csv file
	def save_offsets(self,offset_list,path_to_csv):
		with open(path_to_csv, 'wb') as output:
			wr = csv.writer(output)
			wr.writerow(['lateral_offset','vertical_offset'])
			for row in offset_list:
  			  	wr.writerow(row)
  	
  	#read apparent offset measurements in a csv file wrote by this script
	def read_offsets_file(self,csv_file):
		with open(csv_file, 'rb') as f:
			reader = csv.reader(f)
			read_list = map(tuple, reader)
		offset_list=[]
		for offset in read_list[1:]:
			offset_list.append((float(offset[0]),float(offset[1])))
		return offset_list
	
	#compute the n*(n-1)/2 offset measurements
	def offset_measurement(self,list_vector):
		step_value = 100./(len(list_vector)+(len(list_vector)*(len(list_vector)-1)/2))
		a,b=[],[]
		for vect in list_vector:
			x = [vect[0],0]
			y = [0,vect[1]]
			a.append(stats.linregress(x,y)[0])
			b.append(stats.linregress(x,y)[1])
			self.progressbar.step(step_value)
			self.progressbar.update_idletasks()
		
		i=0
		lateral_offset,vertical_offset = [],[]
		while i < len(a):
			j=0
			while j < len(a):
				if i < j:
					a4int=np.array([[-a[i],1],[-a[j],1]])
					b4int=np.array([[b[i]],[b[j]]])
					lateral_offset.append(np.linalg.solve(a4int,b4int)[0][0])
					vertical_offset.append(np.linalg.solve(a4int,b4int)[1][0])
					self.progressbar.step(step_value)
					self.progressbar.update_idletasks()
				j=j+1
			i=i+1
		
		return a,b,lateral_offset,vertical_offset
	
	##### Remove outliers using Mahalanobis distance
	#from https://github.com/AlexeyMK/senior_design/blob/master/mahalanobis.py
	#and http://kldavenport.com/mahalanobis-distance-and-outliers/
	def MahalanobisDist(self,x, y):
		covariance_xy = np.cov(x,y, rowvar=0)
		inv_covariance_xy = np.linalg.inv(covariance_xy)
		xy_mean = np.mean(x),np.mean(y)
		x_diff = np.array([x_i - xy_mean[0] for x_i in x])
		y_diff = np.array([y_i - xy_mean[1] for y_i in y])
		diff_xy = np.transpose([x_diff, y_diff])		
		md = []
		for i in range(len(diff_xy)):
			md.append(np.sqrt(np.dot(np.dot(np.transpose(diff_xy[i]),inv_covariance_xy),diff_xy[i])))
		return md
	
	def MD_removeOutliers(self,x, y,pc):
		MD = self.MahalanobisDist(x, y)
		threshold = math.sqrt(scipy.stats.chi2.ppf(pc,2))	#Gallego et al.,2013,On the Mahalanobis Distance Classification Criterion for Multidimensional Normal Distributions,p.4391
		new_x, new_y, outliers = [], [], []
		for i in range(len(MD)):
			if MD[i] <= threshold:
				new_x.append(x[i])
				new_y.append(y[i])
			else:
				outliers.append(i) # position of removed pair
		return (new_x, new_y,threshold, outliers)
	
	#return mean and error of 2D data
	def mean_and_error(self,points,confidence_interval_percent):
		pos = points.mean(axis=0)
		confidence_coef = scipy.stats.norm.interval(confidence_interval_percent, loc=0, scale=1)[1]
		sem_x,sem_y = confidence_coef*stats.sem(points,axis=0)
		return pos[0],pos[1], sem_x, sem_y
		
	#save parameters and results
	def save_metada(self,param_results_list,path_to_csv):
		path_to_txt = os.path.splitext(path_to_csv)[0]+"_SSVinfo.txt"
		with open(path_to_txt, 'w') as export:
			for line in param_results_list:
				export.write('{}\n'.format(line))
		#with open(path_to_txt, 'wb') as output:
		#	wr = csv.writer(output, delimiter ='')
		#	for row in param_results_list:
  		#	  	wr.writerow(row)
	
	#draw 1D and 2D histograms
	def draw_fig(self,a,b,lateral_offset,vertical_offset,result,hist2dres=None,xbinwidth=None,ybinwidth=None):
		nullfmt   = NullFormatter()
		mpl.rcParams.update({'font.size': 8})
		# definitions for the axes
		left, width = 0, 0.70
		bottom, height = 0.1, 0.50
		bottom_h = left_h = left+width+0.02
		rect_hist2d = [left, bottom, width, height]
		rect_histx = [left+0.175,bottom+height+0.02 , 0.50+0.025, 0.25]
		rect_histy = [left_h, bottom, 0.25, height]
		# start with a rectangular Figure
		self.fig = plt.figure(1, figsize=(6,6))
		self.canvas.get_tk_widget().destroy()
		self.canvas = FigureCanvasTkAgg(self.fig,master=self.mainFrame)
		#axis definition
		axHist2d = plt.axes(rect_hist2d)
		axHistx = plt.axes(rect_histx)
		axHisty = plt.axes(rect_histy)
		# no labels
		axHistx.xaxis.set_major_formatter(nullfmt)
		axHisty.yaxis.set_major_formatter(nullfmt)
		
		#plot lines
		coords_graph=[]
		i=0
		while i < len(a) :
			coords_graph.append(([int(min(lateral_offset)),0,int(max(lateral_offset))],[int(a[i]*min(lateral_offset)+b[i]),int(b[i]),int(a[i]*max(lateral_offset)+b[i])]))
			i=i+1
		for coords in coords_graph:
			axHist2d.plot(coords[0],coords[1],c="#00FF00",linestyle='--',linewidth=0.25,zorder=1)
		
		#plot 2d histogram
		if hist2dres is None:
			im = axHist2d.hexbin(lateral_offset,vertical_offset,bins='log', cmap=plt.cm.jet,zorder=2, mincnt=1)
			hist2dres = 100
		else:
			im = axHist2d.hexbin(lateral_offset,vertical_offset,bins='log',gridsize=hist2dres, cmap=plt.cm.jet,zorder=2, mincnt=1)
		
		etiq = [10,100,1000,10000,100000,100000]
		log10_etiq = []
		for e in etiq :
			log10_etiq.append(math.log10(e))
		cb = plt.colorbar(im,ax=axHist2d,ticks=log10_etiq,location='left')
		cb.ax.set_yticklabels(etiq,rotation=90)
		cb.ax.yaxis.set_ticks_position('left')
		axHist2d.set_xlim( (min(lateral_offset), max(lateral_offset)) )
		axHist2d.set_ylim( (min(vertical_offset), max(vertical_offset)) )
		axHist2d.set_ylabel('Vertical offset (m)')
		labels = axHist2d.get_yticklabels()
		for label in labels:
			label.set_rotation(90)
		axHist2d.set_xlabel('Lateral offset (m)')
		axHist2d.text(0.05, 0.95,self.txt_legend, ha='left', va='top', fontsize = 8, fontweight='bold', transform=axHist2d.transAxes)
		bin_area= 6*(((max(axHist2d.get_ylim())-min(axHist2d.get_ylim()))/2/hist2dres)*((max(axHist2d.get_xlim())-min(axHist2d.get_xlim()))/2/hist2dres)/2)
		cb.set_label(r'Counts (bin area = ~'+"%.0f" % bin_area+ r'm$^2$)')
		# lateral offset histogram
		if xbinwidth is None:
			axHistx.hist(lateral_offset,log=True)
			xbinwidth = (max(lateral_offset)-min(lateral_offset))/10
		else:	
			xymax = np.max( [np.max(np.fabs(lateral_offset)), np.max(np.fabs(vertical_offset))] )
			lim = ( int(xymax/xbinwidth) + 1) * xbinwidth
			bins = np.arange(-lim, lim + xbinwidth, xbinwidth)
			axHistx.hist(lateral_offset,log=True, bins=bins)
		axHistxLim1 = axHistx.get_ylim()
		axHistx.set_ylim(0.1,axHistxLim1[1])
		axHistx.set_xlim( axHist2d.get_xlim() )
		axHistx.set_ylabel('Counts\n(bin size = '+ str(round(xbinwidth,1))+ r'm)')
		#vertical offset histogram
		if ybinwidth is None:
			axHisty.hist(vertical_offset, log=True, orientation='horizontal')
			ybinwidth=(max(vertical_offset)-min(vertical_offset))/10
		else:
			xymax = np.max( [np.max(np.fabs(lateral_offset)), np.max(np.fabs(vertical_offset))] )
			lim = ( int(xymax/ybinwidth) + 1) * ybinwidth
			bins = np.arange(-lim, lim + ybinwidth, ybinwidth)	
			axHisty.hist(vertical_offset, bins=bins, log=True, orientation='horizontal')
		axHisty.get_xaxis().set_ticks_position('top')
		axHisty.set_xlabel('Counts\n(bin size = '+ str(round(ybinwidth,1))+ r'm)')
		axHisty.xaxis.set_label_position('top')
		axHistyLim1 = axHisty.get_xlim()
		axHisty.set_xlim(0.1,axHistyLim1[1])
		axHisty.set_ylim( axHist2d.get_ylim())
		
		
		
		plt.savefig(result,bbox_inches='tight')
		self.canvas._tkcanvas.grid(column=5, row=self.rowgraph, rowspan=13, columnspan=3, sticky="EW")
		self.canvas.draw()
		self.redrawButton.config(state='normal')
		plt.close('all')
	
	def launch(self) :
		if self.hist2dres.get() == "" :
			self.hist2dres.set(100)
			self.erreur('Number of hexagone\nalong x-axis in 2D histogramm\nset to 100')
 		if self.histlat.get() == ""  :
 			self.histlat.set(10)
 			self.erreur('Bin size of\nlateral offset histogram\nset to 10 meters')
 		if self.histvert.get() == "" :
 			self.histvert.set(10)
 			self.erreur('Bin size of\nvertical offset histogram\nset to 10 meters')
 		if self.outliers.get() == "" :
 			self.outliers.set(0.99)
 			self.erreur('Remove outliers set to 1 percentile')
 		if self.meanconf.get() == ""   :
 			self.meanconf.set(0.95)
 			self.erreur('Confidence level of the standard\nerror of the mean offset\nset to 95%')
		if self.check.get() == 0:
			if self.DEMFile.get() == "" :
				self.erreur('Please select DEM/DSM.')
			elif self.faultShapefile.get() == "" :
				self.erreur('Please select fault(s) shapefile.')
			elif self.contourShapefile.get() == "" :
				self.erreur('Please select contour lines shapefile.')
			elif self.confidenceShapefile.get() == "" :
				self.erreur('Please select excluded area(s) shapefile.')
			elif self.distance.get() == "" :
				self.erreur('Please specify maximum distance from fault (defaut 50 m).')
			elif self.offsetSave.get() == "" :
				self.erreur('Please select backup file.')
			elif self.figsave.get() == "" :
				self.erreur('Please select figure save file.')
			else :
				self.progressbar.configure(value = 0)
				self.progressLabel.configure(text="Apparent offset\nmeasurements progress",state='normal')
				self.params_results_list=["Input:","    DEM/DSM: "+self.DEMFile.get(),"    Fault shapefile: "+self.faultShapefile.get(),"    Contour lines shapefile: "+self.contourShapefile.get(),"    Excluded area(s) shapefile: "+self.confidenceShapefile.get(),"    Distance max from fault: "+str(self.distance.get()),"Output:","    Apparent offset measurements file: "+self.offsetSave.get(),"    Figure: "+self.figsave.get()]
				#apparent offset measurements
				self.vect_possible_x_z=self.apparent_offset_measurements(self.faultShapefile.get(),self.confidenceShapefile.get(),self.DEMFile.get(),self.contourShapefile.get(),self.distance.get())
				
				#save apparent offset measurements in csv file
				self.save_offsets(self.vect_possible_x_z,self.offsetSave.get())
		else:
			if self.offsetCSV.get() == "" :
				self.erreur('Please select offsets measurement CSV file.')
			elif self.figsave.get() == "" :
				self.erreur('Please select figure save file.')
			else:
				self.params_results_list=["Input:","    Apparent offset measurements file: "+self.offsetSave.get(),"Output:","    Figure: "+self.figsave.get()]
				#open apparent offset measurements csv file
				self.vect_possible_x_z=self.read_offsets_file(self.offsetCSV.get())
		
		#offset measurement
		self.progressbar.configure(value = 0)
		self.progressLabel.configure(text="Offset\nmeasurements progress",state='normal')
		self.a,self.b,self.lateral_offset,self.vertical_offset = self.offset_measurement(self.vect_possible_x_z)
		#remove outliers
		self.params_results_list.append("")
		self.params_results_list.append("Outliers set to "+str(self.outliers.get()))
		self.params_results_list.append((" Initial dataset: "+str(len(self.lateral_offset))+" values."))
		self.lateral_offset,self.vertical_offset,self.threshold, self.outliers_values=self.MD_removeOutliers(self.lateral_offset,self.vertical_offset,self.outliers.get())
		self.params_results_list.append((" Dataset without outliers: "+str(len(self.lateral_offset))+" values ("+str(len(self.outliers_values))+" removed)."))
		
		#compute solution
		self.xMean,self.yMean,self.dx,self.dy = self.mean_and_error(np.array([self.lateral_offset,self.vertical_offset]).T,self.meanconf.get())
		self.txt_legend = "Mean:\n-vertical offset: "+"%.2f" % self.yMean+u"\u00B1"+"%.2f" % self.dy+"\n-lateral offset: "+"%.2f" % self.xMean+u"\u00B1"+"%.2f" % self.dx
		print self.txt_legend
		self.params_results_list.append("")
		self.params_results_list.append("Offset values at a "+str(self.meanconf.get())+" confidence level:")
		self.params_results_list.append("    vertical offset: "+"%.2f" % self.yMean+"±"+"%.2f" % self.dy)
		self.params_results_list.append("    lateral offset: "+"%.2f" % self.xMean+"±"+"%.2f" % self.dx)
		self.resultLabel.config(state='normal')
		self.lateralResultLabel.config(state='normal')
		self.verticalResultLabel.config(state='normal')
		self.lateralResultEntry.config(state='normal')
		self.verticalResultEntry.config(state='normal')
		self.lateralResult.set("%.2f" % self.xMean+u"\u00B1"+"%.2f" % self.dx)
		self.verticalResult.set("%.2f" % self.yMean+u"\u00B1"+"%.2f" % self.dy)
		
		self.save_metada(self.params_results_list,self.offsetSave.get())
		
		
		#draw the figure
		self.progressLabel.configure(text="Plotting",state='normal')
		self.progressLabel.update_idletasks()
		self.draw_fig(self.a,self.b,self.lateral_offset,self.vertical_offset,self.figsave.get(),self.hist2dres.get(),self.histlat.get(),self.histvert.get())
		self.progressLabel.configure(text="Done",state='normal')
		

if __name__ == "__main__":
	app = ssvapp_tk(None)
	app.title('SSV Method (Billant et al., 2016)')
	app.mainloop()

