"""Plot aggregate measurement availability from an authorized examinations CSV."""
import argparse, csv
from pathlib import Path
import matplotlib.pyplot as plt
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input_csv');p.add_argument('output_prefix');a=p.parse_args()
    with open(a.input_csv,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    fields=['brachial_d0_cm','brachial_d1_cm','brachial_d2_cm','tibial_d0_cm','tibial_d1_cm','tibial_d2_cm']
    counts=[sum(r.get(k,'')!='' for r in rows) for k in fields]
    fig,ax=plt.subplots(figsize=(7,4)); ax.barh(fields,counts,color='#39749B');ax.set_xlabel('Examinations with available measurement');ax.set_xlim(0,max(len(rows),1));ax.invert_yaxis();fig.tight_layout()
    Path(a.output_prefix).parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(a.output_prefix+'.png',dpi=300);fig.savefig(a.output_prefix+'.pdf');plt.close(fig)
