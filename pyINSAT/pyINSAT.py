import warnings
warnings.filterwarnings("ignore")
import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import xarray as xr
import glob
import pandas as pd
from scipy.interpolate import griddata
import calendar

X, Y = np.arange(50,100,0.1), np.arange(0,50,0.1)
X1,Y1 = np.meshgrid(X,Y)
levs = [1000,950,920,850,780,700,620,500,400,300,250,200,150,100]
nul = xr.DataArray(np.zeros([500, 500], dtype=int),coords=[Y,X], dims=['lat','lon'])
nul = nul.where(nul!=0, np.nan)
nul = xr.DataArray(np.zeros([14,500, 500], dtype=int),coords=[levs,Y,X], dims=['lev','lat','lon'])
nul_3d = nul.where(nul!=0, np.nan)

def INSAT3D_PROF(mole,time,dt, input_dir='',output_dir=''):
    for i in range(0,len(dt)):
        files = sorted(glob.glob(''+str(input_dir)+'3DSND_'+dt[i].strftime('%d')+''+calendar.month_abbr[int(dt[i].strftime('%m'))].upper()+'20'+dt[i].strftime('%y')+'_'+str(time)+'*.h5'))
        if files == []:
            print(''+str(mole)+'','NO_DATA')
            dat = nul_3d
            dat.to_netcdf(''+str(output_dir)+''+str(mole)+'_20'+str(dt[i].strftime('%y'))+''+str(dt[i].strftime('%m'))+''+str(dt[i].strftime('%d'))+'.nc')
        else:
            try:
                for d in files[0:1]:
                    print(d)
                    a = h5py.File(d, mode='r')
                    lat,lon = np.array(a["Latitude"])*0.01, np.array(a["Longitude"])*0.01
                    Z = np.array(a[''+str(mole)+''])
                    leev = np.array(a['plevels']).tolist()
                    jj1 = []
                    for e in levs:
                        jj1.append(leev.index(e))
                    zz = []
                    for h in jj1:
                        try:
                            print(h,''+str(mole)+'','DONE!!!!!')
                            Z = np.array(a[''+str(mole)+''])[0,h,:,:]
                            points = np.array( (lon.flatten(), lat.flatten()) ).T
                            values = Z.flatten()
                            Z0 = griddata( points, values, (X1,Y1), method='nearest' )
                            z1 = np.array(Z0)
                            z1[z1<0] = np.nan
                            zz.append(np.array(z1))  
                        except:
                            print(h,''+str(mole)+'','NO_PROF')
                            zz.append(np.array(nul))
                    z2 = np.array(zz)
                    dat = xr.DataArray(z2, coords=[levs, Y, X], dims=['lev','lat','lon'])
                    dat.to_netcdf(''+str(output_dir)+''+str(mole)+'_20'+str(dt[i].strftime('%y'))+''+str(dt[i].strftime('%m'))+''+str(dt[i].strftime('%d'))+'.nc')
                    zz = []
            except:
                pass

def INSAT3D_TC(mole,time,dt, input_dir='',output_dir=''):
    for i in range(0,len(dt)):
        files = sorted(glob.glob(''+str(input_dir)+'3DSND_'+dt[i].strftime('%d')+''+calendar.month_abbr[int(dt[i].strftime('%m'))].upper()+'20'+dt[i].strftime('%y')+'_'+str(time)+'*.h5'))
        if files == []:
            dat = nul
            print(dat)
            dat.to_netcdf(''+str(output_dir)+''+str(mole)+'_20'+str(dt[i].strftime('%y'))+''+str(dt[i].strftime('%m'))+''+str(dt[i].strftime('%d'))+'.nc')
        else:
            for q in files:
                print(q)
                a =  h5py.File(q, mode='r') 
                lat,lon = np.array(a["Latitude"])*0.01, np.array(a["Longitude"])*0.01
                Z = np.array(a[''+str(mole)+''])
                points = np.array( (lon.flatten(), lat.flatten()) ).T
                values = Z.flatten()
                Z0 = griddata( points, values, (X1,Y1), method='nearest' )
                z1 = np.array(Z0)
                z1[z1<0] = np.nan
                dat = xr.DataArray(z1, coords=[Y,X], dims=['lat','lon'])
                dat.to_netcdf(''+str(output_dir)+''+str(mole)+'_20'+str(dt[i].strftime('%y'))+''+str(dt[i].strftime('%m'))+''+str(dt[i].strftime('%d'))+'_'+str(time)+'.nc')
