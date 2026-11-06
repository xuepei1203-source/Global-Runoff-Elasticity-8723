"""Figure 5: seasonal univariate GAM relationships, hemispherically aligned."""
import numpy as np
import matplotlib.pyplot as plt
from pygam import LinearGAM,s
from _common import FEATURES21,SEASONS,COLORS,STYLES,MARKERS,FIGURES,seasonal_data,season_values

def main():
 df=seasonal_data();fig,axs=plt.subplots(7,3,figsize=(12.6,16.8)); ymax=0
 for i,(ax,feature) in enumerate(zip(axs.flat,FEATURES21)):
  for j,season in enumerate(SEASONS):
   yy=season_values(df,season);xx=df[feature].to_numpy();mask=np.isfinite(yy)&np.isfinite(xx)
   if mask.sum()<20:continue
   gam=LinearGAM(s(0)).fit(xx[mask,None],yy[mask]);grid=np.linspace(-1,1,100);pred=gam.predict(grid[:,None]);ymax=max(ymax,float(np.nanmax(pred)))
   ax.plot(grid,pred,color=COLORS[j],ls=STYLES[j],marker=MARKERS[j],markevery=8,ms=2.5,lw=1.5,label=season)
  ax.set_title(f'({chr(97+i)}) {feature}',fontsize=9);ax.set_xlim(-1,1);ax.tick_params(labelsize=7)
 for ax in axs.flat:ax.set_ylim(0,max(ymax,1e-6)*1.02)
 handles,labels=axs[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=4)
 fig.tight_layout(rect=[0,.03,1,1]);fig.savefig(FIGURES/'figure_05_seasonal_gam_relationships.png',dpi=300,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
