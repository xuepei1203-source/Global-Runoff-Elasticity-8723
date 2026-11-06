"""Figure 7: dominant fitted GAM term contribution for each catchment."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
from pygam import LinearGAM,s
from _common import FEATURES23,read_csv,FIGURES,RESULTS

def main():
 df=read_csv('input_features_normalized.csv',FEATURES23+['elasticity','lon','lat']);X=df[FEATURES23].to_numpy();y=df.elasticity.to_numpy()
 terms=s(0)
 for i in range(1,len(FEATURES23)):terms+=s(i)
 gam=LinearGAM(terms).fit(X,y)
 eff=np.vstack([gam.partial_dependence(term=i,X=X).ravel() for i in range(len(FEATURES23))]).T
 a=np.abs(eff);idx=a.argmax(axis=1);df['dominant_factor_multigam']=np.asarray(FEATURES23)[idx];df['dominant_value_multigam']=a[np.arange(len(df)),idx]
 counts=df.dominant_factor_multigam.value_counts();top=counts.head(6).index.tolist();df['plot_category']=df.dominant_factor_multigam.where(df.dominant_factor_multigam.isin(top),'Other')
 df.to_csv(RESULTS/'figure_07_dominant_drivers.csv',index=False)
 cmap=plt.get_cmap('RdBu_r',6);colors={name:cmap(i) for i,name in enumerate(top)}
 fig,ax=plt.subplots(figsize=(18,9),subplot_kw={'projection':ccrs.PlateCarree()});ax.coastlines('110m',linewidth=.7);ax.set_extent([-180,180,-60,90]);ax.set_xticks([]);ax.set_yticks([])
 for name in ['Other']+top:
  sub=df[df.plot_category==name];ax.scatter(sub.lon,sub.lat,s=10,alpha=.5 if name=='Other' else .8,color='#D3D3D3' if name=='Other' else colors[name],transform=ccrs.PlateCarree(),rasterized=True)
 handles=[mpatches.Patch(color=colors[n],label=f'{n} (n={counts[n]})') for n in top]
 ax.legend(handles=handles,loc='lower left',bbox_to_anchor=(.02,.02),ncol=2,fontsize=9,title='Dominant Factor',frameon=True,facecolor='white',edgecolor='black')
 fig.tight_layout();fig.savefig(FIGURES/'figure_07_global_dominant_drivers.png',dpi=300,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
