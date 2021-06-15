# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import spacepy
import gitm 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import cmocean
import glob, os
from cartopy import config
import cartopy.crs as ccrs
from matplotlib.backends.backend_pdf import PdfPages
# Pull in the rc from matplotlib to make pretty fonts (LaTeX Fonts)
from matplotlib import rc
from matplotlib import ticker
import matplotlib as mpl

## for debugging
import pdb


# Define a short routine for asking inputs
def ask_user(question):
    check = str(input(question+' (y/n): ')).lower().strip()
    if check[:1] == 'y':
       return True
    if check[:1] == 'n':
       return False
    else:
       print('Invalid Input')
       return ask_user("LMAO.. No really, Plot Log?")


# First, we find all 1DALL binary files in the directory and then
# we simply access the first one.

# Set some global parameters for Text
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
mpl.rcParams["lines.linewidth"] = 1.5
mpl.rcParams["contour.negative_linestyle"]='dashed'


# Turn off Interactive MODE (Suppresses the Figures when writing files)
plt.ioff()

# ACCESS GITM DATA FILES
# FILE 1
#print('===> Searching Working Directory for GITM 3DALL Files. \n')
filelist = []  # initialize a filelist array
for file in glob.glob("1DALL*.bin"):
    filelist.append(file)
    
# Sort the Files by date
filelist.sort()
if len(filelist) > 0:
   print('===> Identified ', len(filelist), ' Gitm Binary Files.\n')
   testfile = []
   for file in filelist:
       testfile.append(file)
       #print(file)
else:
    print("!!! Couldn't find any 3DALL*.bin GITM files !!!!")
    raise Exception()
    
gdata = gitm.GitmBin(testfile[len(filelist) - 1])
nVars = gdata.attrs['nVars']
# Pull out the keys (Variable Names) to use
Variables = gdata.keys()
VariableNames = list(Variables)

for iVar in range(nVars-2):
    print('[',iVar,']   ',VariableNames[iVar+3])



UserSelectionString = input("Pick a Variable to Plot [Enter Number]:  ")
iUser_ = int(UserSelectionString) + 3
UserKey = VariableNames[iUser_]
print(' \n')
print('You want to Plot: ',UserKey,'\n')
PI = np.pi

OrignAlts = gdata.attrs['nAlt']

# Pull out actual data
alts = gdata['Altitude' ][0     ,0     ,0:OrignAlts]/1000.0    # Alts in km
nAlts = len(alts)

# Next, Cycle through each 1D file an
nTimes = len(filelist)
nGCs = 3
# Set the shape of our array
array_shape = (nTimes, nAlts)
VariableTimeSeries = np.zeros(array_shape,order='F')
for iFile in range(nTimes):
    gdata = gitm.GitmBin(testfile[iFile])
    VariableTimeSeries[iFile,0:nAlts] = gdata[UserKey][0,0,0:nAlts]

# Now we have the Time Series of the Selected Variable
VariableString = UserKey

question = " Plot Logarithmically? "
plotlog = ask_user(question)
 
TimeAvgVariable = np.sum(VariableTimeSeries, axis=0)/nTimes   # Our Zonal Mean

axis_text_size = 18
title_text_size = 28
tick_font_size = 13
pdfile = '1D_TimeSeries_' + UserKey.strip() + '.pdf'
TitleString = 'Time Series Mean ' + UserKey.strip() 
if plotlog == True:

   fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8.5,8.5),sharex=True)
   line1, = ax.plot(TimeAvgVariable, alts)
   ax.tick_params(axis='both',labelsize=tick_font_size)    
   ax.set_title(TitleString,size = title_text_size)   
   ax.set_xlabel(''+UserKey,size = axis_text_size)
   ax.set_ylabel('Altitude (km)',size = axis_text_size)
   plt.xscale("log")

   plt.show()
   plt.close()


else:

   fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8.5,8.5),sharex=True)
   line1, = ax.plot(TimeAvgVariable, alts)
   ax.tick_params(axis='both',labelsize=tick_font_size)    
   ax.set_title(TitleString,size = title_text_size)   
   ax.set_xlabel(''+UserKey,size = axis_text_size)
   ax.set_ylabel('Altitude (km)',size = axis_text_size)

   plt.show()
   plt.close()

