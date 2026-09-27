"""Public monthly measurement illustration; no causal, futures or trading inference."""
from __future__ import annotations
import hashlib
import io
from pathlib import Path
from urllib.request import Request, urlopen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results' / 'commodity_household_chain_042'
OUT.mkdir(parents=True, exist_ok=True)
BLS = 'https://www.bls.gov/charts/consumer-price-index/consumer-price-index-average-price-data.htm'
WTI = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILWTICO'
ASOF = pd.Timestamp('2026-09-27')

def get(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 research reproducibility'})
    with urlopen(req, timeout=40) as response:
        return response.read()

bls_bytes, wti_bytes = get(BLS), get(WTI)
bls = pd.read_html(io.BytesIO(bls_bytes))[0]
bls['date'] = pd.to_datetime(bls['Month'], format='mixed')
bls = bls.set_index('date').sort_index()
assert bls.index.is_unique and bls.index.max() <= ASOF, 'BLS date QC'
names = {'Bread, white, pan, per lb.':'bread_usd_per_lb',
         'Gasoline, unleaded regular, per gallon':'gas_usd_per_gal'}
price = bls[list(names)].rename(columns=names).apply(pd.to_numeric, errors='coerce')
wti = pd.read_csv(io.BytesIO(wti_bytes))
wti.columns = ['date', 'wti_usd_per_bbl']
wti['date'] = pd.to_datetime(wti['date'])
wti['wti_usd_per_bbl'] = pd.to_numeric(wti['wti_usd_per_bbl'], errors='coerce')
wti = wti[(wti.date <= ASOF) & (wti.date >= price.index.min())]
assert wti.date.is_unique and wti.wti_usd_per_bbl.notna().sum()>200, 'WTI date/coverage QC'
monthly_wti = wti.set_index('date').wti_usd_per_bbl.resample('MS').mean()
price = price.join(monthly_wti, how='outer').rename_axis('date')
price = price.loc['2007-01-01':ASOF]
price.index = price.index.to_period('M').to_timestamp()
assert price.index.is_unique, 'Unique monthly grid QC'
assert (price[['bread_usd_per_lb','gas_usd_per_gal']].stack() > 0).all(), 'Positive retail prices QC'

rows=[]
for year in range(2007, 2026):
    ys=price.loc[str(year)]
    if len(ys) !=12 or ys.isna().any().any():
        continue
    for col in price.columns:
        s=ys[col].to_numpy()
        peak=np.maximum.accumulate(s)
        mdd=np.min(s/peak-1)*100
        future=price.loc[f'{year+1}-01-01':,col].dropna()
        first_recovery=next((str(ix.date()) for ix,val in future.items() if val>=s[0]),None) if s[-1]<s[0] else None
        rows.append({'year':year,'series':col,'jan':round(float(s[0]),4),
                     'dec':round(float(s[-1]),4),'jan_dec_pct':round(float((s[-1]/s[0]-1)*100),2),
                     'within_year_mdd_pct':round(float(mdd),2),
                     'max_above_jan_pct':round(float((np.max(s)/s[0]-1)*100),2),
                     'peak_month':int(np.argmax(s)+1),
                     'end_below_jan':bool(s[-1]<s[0]),
                     'first_month_after_dec_back_above_jan':first_recovery})
panel=pd.DataFrame(rows)
assert set(panel.groupby('year').size())=={3}, 'Common-year QC'
dist=panel.groupby('series').agg(n=('year','size'),median=('jan_dec_pct','median'),
         p10=('jan_dec_pct',lambda x:np.percentile(x,10)),
         p90=('jan_dec_pct',lambda x:np.percentile(x,90)),
         negative_share=('jan_dec_pct',lambda x:(x<0).mean()),
         median_mdd=('within_year_mdd_pct','median')).round(2)

price.to_csv(OUT/'MONTHLY_ALIGNED_PUBLIC_PRICES.csv',float_format='%.5f')
panel.to_csv(OUT/'COMPLETE_YEAR_PATH_PANEL.csv',index=False)
dist.to_csv(OUT/'FULL_SAMPLE_DISTRIBUTION.csv')
fig,axes=plt.subplots(1,3,figsize=(13.4,4.25),sharey=True)
for ax,year in zip(axes,[2008,2020,2022]):
    yr=price.loc[str(year)]
    for col,label in [('wti_usd_per_bbl','WTI spot monthly mean'),
                      ('gas_usd_per_gal','Gasoline retail'),('bread_usd_per_lb','White bread retail')]:
        ax.plot(range(1,13),100*yr[col].to_numpy()/yr[col].iloc[0],label=label,linewidth=2)
    ax.axhline(100,color='grey',linewidth=.7)
    ax.set_title(str(year));ax.set_xticks([1,3,5,7,9,11]);ax.set_xlim(1,12);ax.grid(alpha=.2)
axes[0].set_ylabel('January = 100 (current-vintage retrospective)')
axes[1].set_xlabel('Calendar month')
axes[-1].legend(frameon=False,fontsize=8,loc='upper left')
fig.suptitle('Raw crude, pump price and bread: different clocks (descriptive)')
fig.tight_layout();fig.savefig(OUT/'CASE_YEAR_PRICE_PATHS.png',dpi=170);plt.close(fig)

qc={'bls_url':BLS,'bls_sha256':hashlib.sha256(bls_bytes).hexdigest(),
    'wti_url':WTI,'wti_sha256':hashlib.sha256(wti_bytes).hexdigest(),
    'bls_source_last_month':str(bls.index.max().date()),
    'wti_last_observation':str(wti.date.max().date()),
    'monthly_common_last':str(price.index.max().date()),
    'complete_years':list(map(int,sorted(panel.year.unique()))),
    'incomplete_years':{str(y):[str(x.date()) for x in price.loc[str(y)].index[price.loc[str(y)].isna().any(axis=1)]]
                        for y in [2025,2026] if str(y) in price.index.strftime('%Y').tolist()},
    'rows':len(panel),'qc':'PASS_DESCRIPTIVE_ONLY'}
import json
(OUT/'QC.json').write_text(json.dumps(qc,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(qc,ensure_ascii=False))
print(panel[panel.year.isin([2008,2020,2022])].to_string(index=False))
print(dist.to_string())
