"""Descriptive IMF global grain spot benchmark context; retain no redistributed raw observations."""
from pathlib import Path
from urllib.request import Request, urlopen
import io, hashlib, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parents[1]/'results'/'commodity_household_chain_042'
OUT.mkdir(parents=True,exist_ok=True)
ids={'wheat':'PWHEAMTUSDM','corn':'PMAIZMTUSDM','soybeans':'PSOYBUSDM'}
series={}; provenance={}
for name,ident in ids.items():
    url=f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={ident}'
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=40) as f: raw=f.read()
    d=pd.read_csv(io.BytesIO(raw))
    d.columns=['date',name]
    d['date']=pd.to_datetime(d['date'])
    d[name]=pd.to_numeric(d[name],errors='coerce')
    d=d[d.date<=pd.Timestamp('2026-09-27')]
    assert d.date.is_unique and d[name].dropna().gt(0).all()
    series[name]=d.set_index('date')[name]
    provenance[name]={'url':url,'sha256':hashlib.sha256(raw).hexdigest(),
                      'last_observation':str(d.date.max().date()),'units':'nominal USD/metric ton, IMF global benchmark'}
p=pd.concat(series.values(),axis=1)
p.columns=list(series)
records=[]
for year in range(2007,2025):
    y=p.loc[str(year)]
    assert len(y)==12 and y.notna().all().all(),f'incomplete year {year}'
    for name in ids:
        x=y[name].to_numpy(); peak=np.maximum.accumulate(x)
        records.append({'year':year,'series':name,
          'jan_dec_pct':round(float((x[-1]/x[0]-1)*100),2),
          'within_year_mdd_pct':round(float((x/peak-1).min()*100),2),
          'max_above_jan_pct':round(float((x.max()/x[0]-1)*100),2),
          'peak_month':int(x.argmax()+1)})
panel=pd.DataFrame(records)
dist=panel.groupby('series').agg(n=('year','size'),median=('jan_dec_pct','median'),
    p10=('jan_dec_pct',lambda z:np.percentile(z,10)),p90=('jan_dec_pct',lambda z:np.percentile(z,90)),
    negative_share=('jan_dec_pct',lambda z:(z<0).mean()),median_mdd=('within_year_mdd_pct','median')).round(2)
panel.to_csv(OUT/'IMF_GRAIN_ANNUAL_DERIVED.csv',index=False)
dist.to_csv(OUT/'IMF_GRAIN_FULL_SAMPLE_DISTRIBUTION.csv')
fig,axes=plt.subplots(1,3,figsize=(13.4,4.25),sharey=True)
for ax,yr in zip(axes,[2008,2020,2022]):
    y=p.loc[str(yr)]
    for name in ids:ax.plot(range(1,13),100*y[name].to_numpy()/y[name].iloc[0],label=name,linewidth=2)
    ax.set_title(str(yr)); ax.axhline(100,color='grey',linewidth=.7);ax.grid(alpha=.2)
    ax.set_xticks([1,4,7,10],['Jan','Apr','Jul','Oct']);ax.set_xlim(1,12)
axes[0].set_ylabel('January = 100, IMF global benchmarks')
axes[-1].legend(frameon=False,fontsize=8)
fig.suptitle('Wheat, corn and soybeans: monthly global spot benchmarks (not tradable futures)')
fig.tight_layout();fig.savefig(OUT/'IMF_GRAIN_CASE_PATHS.png',dpi=170);plt.close(fig)
(OUT/'IMF_GRAIN_PROVENANCE.json').write_text(json.dumps({'qc':'PASS_DESCRIPTIVE_ONLY',
 'source':'IMF Primary Commodity Prices via FRED','attribution_required':True,'series':provenance,
 'derived_rows':len(panel),'case_years':[2008,2020,2022]},indent=2)+'\n')
print(panel[panel.year.isin([2008,2020,2022])].to_string(index=False))
print(dist.to_string())
