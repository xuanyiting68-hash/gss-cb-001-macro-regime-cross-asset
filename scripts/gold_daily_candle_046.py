#!/usr/bin/env python3
"""Draw private daily OHLC review charts and a public derived-statistics card.

Inputs are external Stooq CSVs passed explicitly on the command line. Vendor
rows and the detailed candlestick image are never written to the public repo.
"""
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
import numpy as np
import pandas as pd


def load_csv(path):
    d = pd.read_csv(path, parse_dates=["Date"]).set_index("Date").sort_index()
    assert list(d.columns) == ["Open", "High", "Low", "Close"]
    assert d.index.is_unique and d.index.is_monotonic_increasing
    assert d.notna().all().all() and (d > 0).all().all()
    assert (d.High >= d[["Open", "Low", "Close"]].max(axis=1)).all()
    assert (d.Low <= d[["Open", "High", "Close"]].min(axis=1)).all()
    return d


def calculate(d, start, end):
    w = d.loc[start:end]
    assert len(w) > 250
    close_dd = w.Close / w.Close.cummax() - 1
    trough = close_dd.idxmin()
    peak = w.loc[:trough].Close.idxmax()
    future = d.loc[trough:]
    recovered = future[future.Close >= w.loc[peak, "Close"]]
    recovery = recovered.index[0] if len(recovered) else None
    five_run = future.Close.ge(w.loc[peak, "Close"]).rolling(5).sum().eq(5)
    five_end = five_run[five_run].index[0] if five_run.any() else None
    five_start = future.index[future.index.get_loc(five_end)-4] if five_end is not None else None
    wick_dd = w.Low / w.High.cummax() - 1
    wick_trough = wick_dd.idxmin()
    wick_peak = w.loc[:wick_trough].High.idxmax()
    return w, dict(rows=len(w), start=start, end=end,
                   peak=str(peak.date()), peak_close=float(w.loc[peak, "Close"]),
                   trough=str(trough.date()), trough_close=float(w.loc[trough, "Close"]),
                   close_drawdown_pct=float(close_dd.min()*100),
                   decline_calendar_days=int((trough-peak).days),
                   decline_trading_days=len(w.loc[peak:trough])-1,
                   recovery=str(recovery.date()) if recovery is not None else None,
                   recovery_calendar_days=int((recovery-trough).days) if recovery is not None else None,
                   recovery_trading_days=len(d.loc[trough:recovery])-1 if recovery is not None else None,
                   first_recovery_close=float(d.loc[recovery,"Close"]) if recovery is not None else None,
                   five_close_run_start=str(five_start.date()) if five_start is not None else None,
                   five_close_run_end=str(five_end.date()) if five_end is not None else None,
                   wick_peak=str(wick_peak.date()), wick_high=float(w.loc[wick_peak, "High"]),
                   wick_trough=str(wick_trough.date()), wick_low=float(w.loc[wick_trough, "Low"]),
                   wick_drawdown_pct=float(wick_dd.min()*100))


def add_candles(ax, d):
    dates = mdates.date2num(d.index.to_pydatetime())
    for x, (_, row) in zip(dates, d.iterrows()):
        color = "#1A8C79" if row.Close >= row.Open else "#CA514B"
        ax.vlines(x, row.Low, row.High, linewidth=.8, color=color, alpha=.9)
        ax.add_patch(Rectangle((x-.40, min(row.Open, row.Close)), .8,
                               max(abs(row.Close-row.Open), .11),
                               facecolor=color, edgecolor=color, alpha=.88))
    ax.plot(d.index, d.Close, color="#193A54", alpha=.4, linewidth=1.3)


def private_chart(d, m, year, hike, path):
    w = d.loc[m["start"]:m["end"]]
    fig = plt.figure(figsize=(13, 10.7), facecolor="#F7F7F3")
    gs = fig.add_gridspec(3, 1, height_ratios=[.52, 5.7, 1.85], hspace=.34)
    title = fig.add_subplot(gs[0]); title.axis("off")
    title.text(.01,.76,f"{year} gold: daily OHLC candles & drawdown",fontsize=22,weight="bold",color="#173047")
    title.text(.01,.05,"XAU/USD · one candle per trading day · close-to-close peak / trough",fontsize=12,color="#566476")
    ax=fig.add_subplot(gs[1]); ax.set_facecolor("#FFFFFF")
    add_candles(ax,w)
    p=pd.Timestamp(m["peak"]); t=pd.Timestamp(m["trough"])
    ax.axvspan(p,t,color="#D35650",alpha=.08)
    ax.axvline(pd.Timestamp(hike),color="#8169B3",lw=1.5,linestyle="--")
    ax.axhline(m["peak_close"],color="#B68A3B",lw=1,linestyle=":",alpha=.9)
    ax.scatter([p],[m["peak_close"]],color="#D19A3F",s=110,zorder=9,edgecolor="white")
    ax.scatter([t],[m["trough_close"]],color="#C7514B",s=110,zorder=9,edgecolor="white")
    ax.annotate(f'Peak close  {m["peak_close"]:,.2f}\n{m["peak"]}',(p,m["peak_close"]),
                xytext=(-110,32) if year=="1999–2000" else (20,26),textcoords="offset points",fontsize=11,color="#785716",
                bbox=dict(boxstyle="round,pad=.5",fc="white",ec="#E0CB9D"),
                arrowprops=dict(arrowstyle="->",color="#B68A3B"))
    ax.annotate(f'Trough close  {m["trough_close"]:,.2f}\n{m["trough"]}',(t,m["trough_close"]),
                xytext=(18,-45),textcoords="offset points",fontsize=11,color="#AE403B",
                bbox=dict(boxstyle="round,pad=.5",fc="white",ec="#E8B6B2"),
                arrowprops=dict(arrowstyle="->",color="#C7514B"))
    ax.text(.98,.95,f'{m["close_drawdown_pct"]:.1f}%\n{m["decline_calendar_days"]} calendar days / {m["decline_trading_days"]} sessions',
            transform=ax.transAxes,ha="right",va="top",color="#B54240",fontsize=17,weight="bold",
            bbox=dict(boxstyle="round,pad=.5",fc="white",ec="#E9DDDB",alpha=.97))
    ax.text(.02,.03,f'Purple = first Fed hike {hike}; thin line = daily closes',transform=ax.transAxes,
            fontsize=10,color="#676576",bbox=dict(fc="white",ec="none",alpha=.9))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.tick_params(axis='x',rotation=0,labelsize=10)
    ax.tick_params(axis='y',labelsize=10)
    ax.set_ylabel("USD per troy ounce",fontsize=11)
    ax.grid(alpha=.16)
    rec=fig.add_subplot(gs[2]);rec.set_facecolor("#FFFFFF")
    rr=d.loc[t:pd.Timestamp(m["five_close_run_end"])]
    rec.plot(rr.index,rr.Close,color="#195A76",lw=1.8)
    rec.axhline(m["peak_close"],color="#B68A3B",linestyle="--",lw=1.4)
    rec.scatter([pd.Timestamp(m["recovery"])],[m["first_recovery_close"]],s=85,color="white",edgecolor="#15806B",linewidth=2,zorder=5)
    rec.scatter([pd.Timestamp(m["five_close_run_end"])],[rr.Close.iloc[-1]],s=85,color="#15806B",zorder=6)
    rec.set_title(f'Open circle: FIRST touch {m["recovery"]}  |  filled: five consecutive closes above old peak, {m["five_close_run_end"]}',
                  loc="left",fontsize=12,pad=10)
    rec.grid(alpha=.15);rec.set_ylabel("Daily close",fontsize=10)
    rec.xaxis.set_major_locator(mdates.MonthLocator(interval=5 if year=="1999–2000" else 2))
    rec.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.text(.04,.025,'Source: Stooq XAUUSD daily OHLC, accessed Sep 28 2026. Personal review only; see separate high-to-low wick result.',fontsize=10,color="#667382")
    fig.savefig(path,dpi=170,bbox_inches='tight',facecolor=fig.get_facecolor());plt.close(fig)


def public_card(a,b,path):
    fig=plt.figure(figsize=(9,13),facecolor="#F6F5F0")
    ax=fig.add_axes([.06,.06,.88,.89]);ax.axis('off')
    ax.text(0,1.04,'Gold after the first Fed hike',fontsize=28,weight='bold',color='#173047',transform=ax.transAxes)
    ax.text(0,1.00,'The final return can hide the pain in between.',fontsize=15,color='#526475',transform=ax.transAxes)
    def block(top,title,m,accent,notice=None):
        ax.add_patch(Rectangle((0,top-.405),1,.40,transform=ax.transAxes,fc='white',ec='#E6E5DD',lw=1))
        ax.text(.04,top-.06,title,transform=ax.transAxes,fontsize=19,weight='bold',color='#173047')
        ax.text(.04,top-.155,f'{m["close_drawdown_pct"]:.1f}%',transform=ax.transAxes,fontsize=40,weight='bold',color=accent)
        ax.text(.38,top-.145,'peak close → later trough close',transform=ax.transAxes,fontsize=13,color='#41556C')
        ax.text(.04,top-.215,f'{m["peak"]}  →  {m["trough"]}',transform=ax.transAxes,fontsize=15,color='#273E55')
        ax.text(.04,top-.275,f'Fell over {m["decline_calendar_days"]} days  ·  recovery took another {m["recovery_calendar_days"]} days',transform=ax.transAxes,fontsize=13,color='#506072')
        ax.text(.04,top-.338,f'First touch {m["recovery"]}  ·  held for 5 closes: {m["five_close_run_end"]}',transform=ax.transAxes,fontsize=12,color='#147C70',weight='bold')
        if notice: ax.text(.04,top-.384,notice,transform=ax.transAxes,fontsize=10.4,color='#A05242')
    block(.94,'1999–2000 first-hike window',a,'#BE5149','Peak followed the June 30 1999 first rate hike.')
    block(.50,'2022–2023 first-hike window',b,'#BE5149','Mar 8 peak PRECEDED Mar 16 first rate hike by eight days.')
    ax.text(.01,.02,'2022 strictly AFTER hike: close drawdown ~18.0%.',fontsize=14,weight='bold',color='#173047',transform=ax.transAxes)
    ax.text(.01,-.025,'Derived statistics, NOT a daily price chart. Windows specified in advance.',fontsize=10,color='#5E6B79',transform=ax.transAxes)
    ax.text(.01,-.058,'Source: Stooq XAUUSD daily history; official FOMC statements.\nHistorical description only: neither Fed causality nor tested trading returns.',fontsize=9.5,color='#5E6B79',transform=ax.transAxes)
    fig.savefig(path,dpi=150,bbox_inches='tight',facecolor=fig.get_facecolor());plt.close(fig)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--historical',type=Path,required=True)
    ap.add_argument('--recent',type=Path,required=True)
    ap.add_argument('--font',type=Path)
    ap.add_argument('--private-out',type=Path,required=True)
    ap.add_argument('--public-out',type=Path,required=True)
    args=ap.parse_args();args.private_out.mkdir(parents=True,exist_ok=True);args.public_out.mkdir(parents=True,exist_ok=True)
    if args.font:
        font_manager.fontManager.addfont(str(args.font))
        plt.rcParams['font.family']=font_manager.FontProperties(fname=str(args.font)).get_name()
    plt.rcParams['axes.unicode_minus']=False
    old=load_csv(args.historical);new=load_csv(args.recent)
    w99,a=calculate(old,'1999-05-01','2000-06-30')
    w22,b=calculate(new,'2022-02-01','2023-03-31')
    _,strict=calculate(new,'2022-03-17','2023-03-16')
    assert a['rows']==301 and b['rows']==301
    assert a['peak']=='1999-10-05' and a['trough']=='2000-05-25' and a['recovery']=='2002-05-31'
    assert b['peak']=='2022-03-08' and b['trough']=='2022-09-26' and b['recovery']=='2023-05-04'
    assert abs(a['close_drawdown_pct']+16.95852534562212)<1e-6
    assert abs(b['close_drawdown_pct']+20.83916761381652)<.01
    private_chart(old,a,'1999–2000','1999-06-30',args.private_out/'GOLD_DAILY_CANDLES_1999_PERSONAL.png')
    private_chart(new,b,'2022–2023','2022-03-16',args.private_out/'GOLD_DAILY_CANDLES_2022_PERSONAL.png')
    public_card(a,b,args.public_out/'GOLD_DAILY_DRAWDOWN_PUBLIC_SUMMARY.png')
    checks={'status':'DESCRIPTIVE_QC_PASS','retrieval_date_sydney':'2026-09-28',
            'historical_source_sha256':hashlib.sha256(args.historical.read_bytes()).hexdigest(),
            'recent_source_sha256':hashlib.sha256(args.recent.read_bytes()).hexdigest(),
            'historical_raw_rows':len(old),'recent_raw_rows':len(new),'1999':a,'2022':b,'2022_strict_after_hike':strict,
            'source_redistribution':'RAW_CSV_AND_PRIVATE_FULL_OHLC_CHART_NOT_FOR_PUBLIC_REPO',
            'public_card_contains':'derived summaries, date markers and no full OHLC paths'}
    (args.public_out/'QC.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:checks[k] for k in ('1999','2022','2022_strict_after_hike')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
