#This program will scan through and collate all the data that evan took as an undergrad on the racetrack project.

#He has saved them in the following directory structure
#/mnt/e/RaceTrack/Data/$DATE$/FILM$FILMNUMBER$/$VOLTAGE$/t1valuematrix.csv

#and what I need is the average velocity (or max velocity of the film) and the voltage of the flowmeter. These are the two important variables. 

#You can't be sure that the path is exactly that, some folders have more in the their chains. But as far as I can tell it is always $VOLTAGE$/t1valuematrix.csv

#So, this should be a fairly straightforward regex process

#Program:
#1. Search for all files named t1valuematrix.csv
#2. Extract voltage from path name
#3. For each file:
#a. plot the velocity profile (to make sure the data is good)
#b. record the average velocity
#c. record the max velocity
#d. record the date
#e. plot all average velocity vs voltage
#f. plot all average velocity vs voltage with numbers as points (do outlier check)
#g. make nice plot
#h. make differences plot


#June 08 2018:
#I am going to aim to do 1 and 2 today


import glob
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mmperpixel=.0041033
def custom_round(x, base=10):
    return int(base * round(float(x)/base))#this sets the width of the bins
i=0
bigdata = []
for filename in glob.iglob('./RaceTrack/**/t1valuematrix.csv',recursive=True): #only for python >3.5
    voltagepattern = re.compile('./RaceTrack/.*/(\d\.\d{,4})/t1valuematrix.csv')
    datepattern = re.compile('./RaceTrack/.*/(\d\d[A-Z]{,4}[a-z]{,4}20\d\d)/.*')
    voltmatch =re.match(voltagepattern,filename) 
    datematch = re.match(datepattern,filename)
    if voltmatch is not None:
        voltage = float(voltmatch.group(1))
        print(voltage)

    #now, read in file
    data =pd.read_csv(filename)
    xmin = data['x'].min()
    xmax = data['x'].max()
    data['xbin'] = data['x'].apply(lambda x: custom_round(x, base=20))
    xgroup = data.groupby('xbin',as_index=False).agg({'dr':['mean','std'],'x':'mean'})
    xgroup.columns=['xbin','dr','std','x']
    xgroup.fillna(0)
#    fig,ax = plt.subplots()
#    ax.errorbar(xgroup['x'].values*mmperpixel,xgroup['dr']*mmperpixel,yerr=xgroup['std']*mmperpixel,fmt='.')
#    plt.show()
    datatosave = [datematch.group(1),float(voltmatch.group(1)),xgroup['dr'].mean()]    
    bigdata.append(datatosave)
    if i >3:
        break
    i=i+1

bigdata = pd.DataFrame(bigdata,columns=['date','voltage','ave velocity'])
bigdata.to_csv('all-evansdata.csv')
    #need to do binning on x data, set each bin to be 10 px wide

#    yspread = 10 #the total range of pixels to include in each slice
#    for i,y in enumerate(np.linspace(0,ymax,num=20)):
#
#        yslice = BigDataNormed[(BigDataNormed['ynormed'] > y) & (BigDataNormed['ynormed'] < y+yspread)]
#        curax = axarr[i/ncols, np.mod(i,ncols)] 
#        for region in set(yslice.region):
#            x = yslice[yslice.region == region].xnormed.values
#            dr =yslice[yslice.region == region].dr.values
#            curax.plot(x,dr,'.',alpha =.3,label='reg='+str(region))
#        curax.axis('off')
#        curax.text(.3,.6,'y='+str(int(y)),fontsize=30,transform=curax.transAxes)
#        curax.legend(loc='best',frameon=False,fontsize=5)
#            
#    plt.tight_layout()
#    f.savefig('allyslices.pdf')
#
#
