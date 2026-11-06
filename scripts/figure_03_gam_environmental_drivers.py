"""Figure 3: univariate GAM relationships for 21 environmental drivers."""
import numpy as np
import matplotlib.pyplot as plt
from pygam import LinearGAM,s
from _common import DATA,FIGURES,FEATURES21,read_csv

def main():
 df=read_csv('input_features_normalized.csv',FEATURES21+['elasticity'])
 fig,axs=plt.subplots(7,3,figsize=(12.6,16.8)); ymax=0
 for i,(ax,name) in enumerate(zip(axs.flat,FEATURES21)):
  x=df[[name]].to_numpy();y=df.elasticity.to_numpy();gam=LinearGAM(s(0)).fit(x,y)
  xx=np.linspace(-1,1,100).reshape(-1,1);pred=gam.predict(xx);ci=gam.confidence_intervals(xx,width=.95)
  ax.plot(xx[:,0],pred,color='blue',lw=1.4);ax.plot(xx[:,0],ci[:,0],'r--',lw=.7);ax.plot(xx[:,0],ci[:,1],'r--',lw=.7)
  ax.set_title(f'({chr(97+i)}) {name}',fontsize=9);ax.set_xlim(-1,1);ymax=max(ymax,float(np.nanmax(ci)))
 for ax in axs.flat:ax.set_ylim(0,max(ymax,1e-6)*1.02);ax.tick_params(labelsize=7)
 axs[-1,0].set_xlabel('Normalised predictor');fig.tight_layout()
 fig.savefig(FIGURES/'figure_03_gam_environmental_drivers.png',dpi=300,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
