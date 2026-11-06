"""Figure 4: composite importance of multivariable GAM fitted term effects."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pygam import LinearGAM,s
from _common import FEATURES21,read_csv,FIGURES,RESULTS

def main():
 df=read_csv('input_features_normalized.csv',FEATURES21+['elasticity']);X=df[FEATURES21].to_numpy();y=df.elasticity.to_numpy()
 terms=s(0)
 for i in range(1,len(FEATURES21)):terms+=s(i)
 gam=LinearGAM(terms).gridsearch(X,y,lam=np.logspace(-2,3,10),progress=False)
 records=[]
 for i,name in enumerate(FEATURES21):
  effect=gam.partial_dependence(term=i,X=X).ravel();sorted_effect=effect[np.argsort(X[:,i])]
  records.append({'Factor':name,'P95_P5':np.percentile(effect,95)-np.percentile(effect,5),'IQR':np.percentile(effect,75)-np.percentile(effect,25),'SD':np.std(effect),'TotalVariation':np.abs(np.diff(sorted_effect)).sum()})
 out=pd.DataFrame(records);metrics=['P95_P5','IQR','SD','TotalVariation']
 for m in metrics:
  lo,hi=out[m].min(),out[m].max();out[m+'_scaled']=(out[m]-lo)/(hi-lo) if hi>lo else 0.
 out['CompositeImportance']=out[[m+'_scaled' for m in metrics]].mean(axis=1)
 out=out.sort_values('CompositeImportance',ascending=False);out.to_csv(RESULTS/'figure_04_gam_driver_importance.csv',index=False)
 fig,ax=plt.subplots(figsize=(9,8));ax.barh(out.Factor[::-1],out.CompositeImportance[::-1],color='black');ax.set_xlabel('Composite GAM term-effect importance');fig.tight_layout()
 fig.savefig(FIGURES/'figure_04_gam_driver_importance.png',dpi=300,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
