from pathlib import Path
from fractions import Fraction as F
from math import prod
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

out=Path(__file__).resolve().parent
s=prod((F(7*j,7*j+1) for j in range(1,8)), start=F(1))
alpha=1-s+F(1,2)
assert alpha==F(6580499,8230200)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.fonttype":"none"})
fig,axs=plt.subplots(1,2,figsize=(14,8),gridspec_kw={"wspace":.65})
fig.patch.set_facecolor("#f8fafc")
fig.subplots_adjust(left=.20,right=.96,top=.75,bottom=.34)
fig.text(.055,.94,"Two exact failures of an acceptance calculation",fontsize=24,weight="bold",color="#15263a")
fig.text(.055,.89,"Successive sampling without replacement · Hu et al., ICLR 2025",fontsize=14,color="#475569")
for ax,title,labels,vals,strings in [
 (axs[0],"4 tokens · 3 drafts",["Published formula","RRS rule, exact replay","Valid verifier"],[95,95.5,100],["95%","95.5%","100%"]),
 (axs[1],"8 tokens · 7 drafts",["Published formula","True optimum"],[100,float(alpha*100)],["100%","79.96%"])
]:
 ax.set_facecolor("#f8fafc")
 colors=["#64748b"]+(["#60a5fa"] if len(vals)==3 else [])+["#0f766e"]
 bars=ax.barh(range(len(vals)),vals,color=colors,height=.5)
 ax.set_yticks(range(len(vals)),labels)
 ax.invert_yaxis();ax.set_xlim(0,113);ax.set_xticks([0,25,50,75,100]);ax.xaxis.set_major_formatter(PercentFormatter(100,decimals=0))
 ax.set_title(title,loc="left",fontsize=16,weight="bold",pad=20,color="#15263a")
 ax.set_xlabel("Acceptance probability",labelpad=10,color="#475569")
 ax.set_axisbelow(True);ax.grid(axis="x",color="#e2e8f0",linewidth=.8)
 for sp in ax.spines.values():sp.set_visible(False)
 ax.tick_params(axis="both",length=0,labelcolor="#334155",pad=9)
 for bar,txt in zip(bars,strings):
  ax.text(bar.get_width()+2,bar.get_y()+bar.get_height()/2,txt,va="center",weight="bold",fontsize=12,color="#15263a")
fig.text(.055,.23,"What fails",fontsize=12,weight="bold",color="#15263a")
fig.text(.055,.19,"The calculation substitutes probabilities from a different without-replacement sampling law.",fontsize=12,color="#334155")
fig.text(.055,.15,"Both examples use strictly positive distributions. Exact rational proofs and separate implementations agree.",fontsize=11,color="#334155")
fig.text(.055,.09,"Scope: acceptance calculations, not measured speedups or corrected experimental tables.",fontsize=10,color="#475569")
fig.text(.055,.055,"Codex-assisted analysis · Specific novelty and external review pending · Research note",fontsize=9,color="#64748b")
for ext in ["png","svg","pdf"]:fig.savefig(out/("acceptance-counterexamples."+ext),dpi=180,facecolor=fig.get_facecolor())
(out/"FIGURE-DATA.json").write_text(json.dumps({"four_token":{"formula":"19/20","rrs":"191/200","valid_verifier":"1"},"eight_token":{"n":7,"q_rare":"1/50","q_each_common":"7/50","p_rare":"1/2","p_each_common":"1/14","formula":"1","successive_optimum":str(alpha),"omission_probability":str(s)},"scope":"Exact constructed distributions, not real-model measurements","private":True},indent=2)+"\n")
