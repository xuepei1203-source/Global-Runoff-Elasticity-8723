"""Supplementary Figure S1: inverse-density weighted multivariable GAM."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
from pygam import LinearGAM,s
from _common import FEATURES23,read_csv,FIGURES,RESULTS
GRID_SIZE=5.;WEIGHT_POWER=.5;TOP_N=6

def main():
 df=read_csv('input_features_normalized.csv',FEATURES23+['elasticity','lon','lat']).reset_index(drop=True)
 df['grid_lon']=np.floor((df.lon+180)/GRID_SIZE).astype(int);df['grid_lat']=np.floor((df.lat+90)/GRID_SIZE).astype(int)
 df['grid_station_count']=df.groupby(['grid_lon','grid_lat']).lon.transform('count')
 w=df.grid_station_count.to_numpy(float)**(-WEIGHT_POWER);w/=w.mean();df['spatial_weight']=w
 X=df[FEATURES23].to_numpy();y=df.elasticity.to_numpy();terms=s(0)
 for i in range(1,len(FEATURES23)):terms+=s(i)
 gam=LinearGAM(terms).fit(X,y,weights=w)
 effects=np.vstack([gam.partial_dependence(term=i,X=X).ravel() for i in range(len(FEATURES23))]).T
 a=np.abs(effects);idx=a.argmax(axis=1);df['dominant_factor_multigam']=np.asarray(FEATURES23)[idx];df['dominant_value_multigam']=a[np.arange(len(df)),idx]
 df.to_csv(RESULTS/'supplementary_s01_dominant_factors.csv',index=False)
 counts=df.dominant_factor_multigam.value_counts();summary=pd.DataFrame({'Factor':counts.index,'Count':counts.values,'Percentage':counts.values/len(df)*100});summary.to_csv(RESULTS/'supplementary_s01_factor_frequency.csv',index=False)
 top=counts.head(TOP_N).index.tolist();cmap=plt.get_cmap('RdBu_r',6);colors={fac:cmap(i) for i,fac in enumerate(top)}
 fig,ax=plt.subplots(figsize=(18,9),subplot_kw={'projection':ccrs.PlateCarree()});ax.coastlines('110m',linewidth=.7);ax.set_extent([-180,180,-60,90]);ax.set_xticks([]);ax.set_yticks([])
 other=df[~df.dominant_factor_multigam.isin(top)];ax.scatter(other.lon,other.lat,s=10,alpha=.5,color='#D3D3D3',transform=ccrs.PlateCarree(),rasterized=True)
 for fac in top:
  sub=df[df.dominant_factor_multigam==fac];ax.scatter(sub.lon,sub.lat,s=10,alpha=.8,color=colors[fac],transform=ccrs.PlateCarree(),rasterized=True)
 handles=[mpatches.Patch(color=colors[fac],label=f'{fac} (n={counts[fac]})') for fac in top]
 ax.legend(handles=handles,loc='lower left',bbox_to_anchor=(.02,.02),ncol=2,fontsize=9,frameon=True,title='Dominant Factor',facecolor='white',edgecolor='black')
 fig.tight_layout();fig.savefig(FIGURES/'supplementary_figure_s01_spatially_weighted_gam.png',dpi=300,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
