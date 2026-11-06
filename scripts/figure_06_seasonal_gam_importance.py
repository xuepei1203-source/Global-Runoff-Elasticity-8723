"""Figure 6: season-wise min-max-normalised univariate GAM importance."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pygam import LinearGAM,s
from _common import FEATURES21,SEASONS,COLORS,FIGURES,RESULTS,seasonal_data,season_values

def main():
 df=seasonal_data();rows=[]
 for season in SEASONS:
  y=season_values(df,season)
  for feature in FEATURES21:
   x=df[feature].to_numpy();mask=np.isfinite(x)&np.isfinite(y)
   if mask.sum()<20:continue
   gam=LinearGAM(s(0)).fit(x[mask,None],y[mask]);lo,hi=np.percentile(x[mask],[1,99]);grid=np.linspace(lo,hi,200)
   eff=gam.partial_dependence(term=0,X=grid[:,None]).ravel()
   rows.append({'Season':season,'Factor':feature,'P95_P5':np.percentile(eff,95)-np.percentile(eff,5),'IQR':np.percentile(eff,75)-np.percentile(eff,25),'SD':np.std(eff),'TotalVariation':np.abs(np.diff(eff)).sum()})
 out=pd.DataFrame(rows);metrics=['P95_P5','IQR','SD','TotalVariation']
 for m in metrics:
  def scale(x):return (x-x.min())/(x.max()-x.min()) if x.max()>x.min() else x*0
  out[m+'_scaled']=out.groupby('Season')[m].transform(scale)
 out['CompositeImportance']=out[[m+'_scaled' for m in metrics]].mean(axis=1);out.to_csv(RESULTS/'figure_06_seasonal_gam_importance.csv',index=False)
 fig,ax=plt.subplots(figsize=(14,6));indices=np.arange(len(FEATURES21));width=.2
 for i,season in enumerate(SEASONS):
  sub=out[out.Season==season].set_index('Factor').reindex(FEATURES21)
  ax.bar(indices+(i-1.5)*width,sub.CompositeImportance,width,color=COLORS[i],label=season)
 ax.set_xticks(indices,FEATURES21,rotation=65,ha='right');ax.set_ylabel('Within-season normalised importance');ax.legend(ncol=4);fig.tight_layout()
 fig.savefig(FIGURES/'figure_06_seasonal_gam_importance.png',dpi=300,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
