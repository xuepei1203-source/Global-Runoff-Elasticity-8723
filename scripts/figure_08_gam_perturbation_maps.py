"""Figure 8: maps of precomputed +10% GAM perturbation effects."""
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from _common import DATA,FIGURES

def main():
 path=DATA/'elasticity_perturbation_10percent.csv'
 if not path.exists():raise FileNotFoundError(path)
 df=pd.read_csv(path);cols=[c for c in df if c.endswith('delta(+10%)')]
 if not cols or len(cols)>21:raise ValueError(f'Expected 1–21 perturbation columns; found {len(cols)}')
 for c in ['lon','lat']+cols:
  if c not in df:raise ValueError(f'Missing column: {c}')
  df[c]=pd.to_numeric(df[c],errors='coerce')
 df=df.dropna(subset=['lon','lat']);values=df[cols].to_numpy(float);finite=values[np.isfinite(values)]
 if not finite.size:raise ValueError('No finite perturbation values')
 absmax=max(float(np.max(np.abs(finite))),1e-9)
 fig=plt.figure(figsize=(8.5,11));sc=None
 for i,col in enumerate(cols):
  row,c=divmod(i,3);ax=fig.add_axes([c/3,.25+(6-row)*(.75/7),1/3,.75/7],projection=ccrs.PlateCarree())
  ax.add_feature(cfeature.COASTLINE,linewidth=.3);ax.set_extent([-180,180,-60,90]);ax.text(.02,.97,f'({string.ascii_lowercase[i]})',transform=ax.transAxes,va='top',fontsize=10)
  sc=ax.scatter(df.lon,df.lat,c=df[col],cmap='RdBu_r',vmin=-absmax,vmax=absmax,s=8,edgecolor='k',linewidth=.1,transform=ccrs.PlateCarree());ax.set_xticks([]);ax.set_yticks([])
 cax=fig.add_axes([.12,.20,.76,.02]);cb=fig.colorbar(sc,cax=cax,orientation='horizontal');cb.set_label('Elasticity Change (GAM +10%)',fontsize=12)
 fig.savefig(FIGURES/'figure_08_gam_perturbation_maps.png',dpi=300,bbox_inches='tight',pad_inches=.02);plt.close(fig)
if __name__=='__main__':main()
