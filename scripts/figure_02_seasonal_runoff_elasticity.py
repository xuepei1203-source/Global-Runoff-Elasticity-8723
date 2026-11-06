"""Figure 2: hemispherically aligned seasonal elasticity maps."""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from _common import read_csv,FIGURES,green_cmap

def main():
 df=read_csv('station_elasticity_seasonal_1950_2015_min40years.csv',['lon','lat','elasticity'])
 if 'season' not in df:raise ValueError('Missing season column')
 df['season']=df.season.astype(str).str.lower().map({'winter':'DJF','spring':'MAM','summer':'JJA','autumn':'SON','djf':'DJF','mam':'MAM','jja':'JJA','son':'SON'})
 positive=df.loc[df.elasticity>0,'elasticity'];vmax=float(np.nanpercentile(positive,98)) if len(positive) else 1.
 fig,axs=plt.subplots(2,2,figsize=(14.5,6.6),subplot_kw={'projection':ccrs.PlateCarree()})
 pairs=[('MAM','SON'),('JJA','DJF'),('SON','MAM'),('DJF','JJA')]
 for i,(ax,(nh,sh)) in enumerate(zip(axs.flat,pairs)):
  mask=((df.lat>=0)&(df.season==nh))|((df.lat<0)&(df.season==sh));sub=df[mask]
  ax.coastlines('110m',linewidth=.4);ax.set_extent([-180,180,-60,90]);ax.set_xticks([]);ax.set_yticks([])
  sc=ax.scatter(sub.lon,sub.lat,c=sub.elasticity,s=9,cmap=green_cmap(),vmin=0,vmax=vmax,transform=ccrs.PlateCarree())
  ax.text(.02,.98,f'({chr(97+i)})',transform=ax.transAxes,va='top')
 fig.colorbar(sc,ax=axs.ravel().tolist(),orientation='horizontal',fraction=.045,pad=.06,label='Runoff Elasticity')
 fig.savefig(FIGURES/'figure_02_seasonal_runoff_elasticity.png',dpi=300,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
