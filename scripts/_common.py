from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed'
RAW = ROOT / 'data' / 'raw'
FIGURES = ROOT / 'outputs' / 'figures'
RESULTS = ROOT / 'outputs' / 'results'
MODELS = ROOT / 'outputs' / 'models'
for d in (FIGURES, RESULTS, MODELS): d.mkdir(parents=True, exist_ok=True)
FEATURES21 = ['PET','Temperature','SoilWaterV1','SoilWaterV4','Snowmelt','TerrainSlope','SaturatedKsat','Drainage_Density','Sub_area','urban','primf','secdn','c3ann','c4ann','c3per','c4per','c3nfx','pastr','range','secmb','secma']
FEATURES23 = ['PET','Temperature','SoilWaterV1','SoilWaterV4','Snowmelt','TerrainSlope','SaturatedKsat','Drainage_Density','Sub_area','urban','primf','primn','secdf','secdn','c3ann','c4ann','c3per','c4per','c3nfx','pastr','range','secmb','secma']
SEASONS = ('Spring','Summer','Autumn','Winter')
COLORS = ('#4DAF4A','#377EB8','#FF7F00','#984EA3')
STYLES = ('-','--','-.',':')
MARKERS = ('o','s','^','D')
def read_csv(name, columns):
 import pandas as pd, numpy as np
 path=DATA/name
 if not path.exists(): raise FileNotFoundError(f'Missing input: {path}. See data/README.md')
 df=pd.read_csv(path)
 missing=set(columns)-set(df.columns)
 if missing: raise ValueError(f'Missing columns in {path.name}: {sorted(missing)}')
 df[columns]=df[columns].apply(pd.to_numeric,errors='coerce')
 return df.replace([np.inf,-np.inf],np.nan).dropna(subset=columns).copy()
def green_cmap():
 import numpy as np, matplotlib.pyplot as plt
 from matplotlib.colors import LinearSegmentedColormap
 return LinearSegmentedColormap.from_list('GreenGrad',plt.get_cmap('YlGn')(np.linspace(.15,.85,256)))
def seasonal_data():
 import pandas as pd
 a=read_csv('input_features_normalized.csv',['lat','lon']+FEATURES21)
 b=read_csv('station_elasticity_seasonal_1950_2015_min40years.csv',['lat','lon','elasticity'])
 if 'season' not in b: raise ValueError('Missing season column')
 b['season']=b['season'].astype(str).str.lower().map({'winter':'DJF','spring':'MAM','summer':'JJA','autumn':'SON','djf':'DJF','mam':'MAM','jja':'JJA','son':'SON'})
 b=b.dropna(subset=['season']).pivot_table(index=['lat','lon'],columns='season',values='elasticity',aggfunc='mean').reset_index()
 a=a.merge(b,on=['lat','lon'],how='inner',validate='many_to_one')
 return a
# hemispheric season mapping: Spring, Summer, Autumn, Winter
SEASON_MAP = {'Spring':('MAM','SON'),'Summer':('JJA','DJF'),'Autumn':('SON','MAM'),'Winter':('DJF','JJA')}
def season_values(df, season):
 import numpy as np
 north,south=SEASON_MAP[season]
 return np.where(df['lat'].to_numpy()>=0,df[north].to_numpy(),df[south].to_numpy())
