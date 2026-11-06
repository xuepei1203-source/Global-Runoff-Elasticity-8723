"""Figure 1: observed annual global runoff elasticity."""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from _common import read_csv,FIGURES,green_cmap

def main():
 df=read_csv('input_features_normalized.csv',['lon','lat','elasticity'])
 fig=plt.figure(figsize=(14.5,7.5)); ax=fig.add_subplot(111,projection=ccrs.PlateCarree())
 ax.coastlines('110m',linewidth=.5);ax.set_extent([-180,180,-60,90])
 sc=ax.scatter(df.lon,df.lat,c=df.elasticity,cmap=green_cmap(),vmin=0,vmax=3.5,s=15,transform=ccrs.PlateCarree())
 ax.set_xticks([]);ax.set_yticks([])
 cb=fig.colorbar(sc,ax=ax,orientation='horizontal',fraction=.045,pad=.05);cb.set_label('Runoff Elasticity')
 fig.savefig(FIGURES/'figure_01_global_runoff_elasticity.png',dpi=400,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
