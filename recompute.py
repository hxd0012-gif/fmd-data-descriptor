"""Recompute 16 measures from one examination; Python 3 standard library only."""
import argparse, csv, math
KEYS = ['subject_id', 'record_id']
def calculate(n,comparators):
    c={}
    def put(k,inputs,fn,positive=()):
        if all(x in n and x not in comparators for x in inputs) and all(n[x]>0 for x in positive):
            v=fn(*[n[x] for x in inputs])
            if math.isfinite(v):c[k+'_calc']=v
    put('bmi',['height_cm','weight_kg'],lambda h,w:w/(h/100)**2,('height_cm','weight_kg'))
    put('bsa_m2',['height_cm','weight_kg'],lambda h,w:.0061*h+.0128*w-.1529,('height_cm','weight_kg'))
    for k,a,b in [('waist_hip_ratio','waist_cm','hip_cm'),('apoa1_apob_ratio','apoa1_g_l','apob_g_l'),('hdl_total_cholesterol_ratio','hdl_mmol_l','total_cholesterol_mmol_l'),('e_over_eprime','mitral_e_m_s','annular_e_m_s'),('e_over_a','mitral_e_m_s','mitral_a_m_s')]:
        put(k,[a,b],lambda x,y:x/y,(b,))
    put('smoking_index_cig_years',['cigarettes_per_day','smoking_years'],lambda x,y:x*y)
    put('alcohol_cumulative_g_day_years',['alcohol_g_per_day','drinking_years'],lambda x,y:x*y)
    for vessel in ('brachial','tibial'):
        for label,idx in [('fmd',1),('nid',2)]:
            put(f'{label}_{vessel}_pct',[f'{vessel}_d0_cm',f'{vessel}_d{idx}_cm'],lambda x,y:100*(y-x)/x,(f'{vessel}_d0_cm',))
    put('lvm_g',['lvdd_cm','ivst_cm','lvpwt_cm'],lambda d,s,p:.8*1.04*((d+s+p)**3-d**3)+.6,('lvdd_cm','ivst_cm','lvpwt_cm'))
    bsa=c.get('bsa_m2_calc')
    if bsa and bsa>0:
        if n.get('cardiac_output_l_min') and 'cardiac_output_l_min' not in comparators:c['cardiac_index_l_min_m2_calc']=n['cardiac_output_l_min']/bsa
        if 'lvm_g_calc' in c:c['lvmi_g_m2_calc']=c['lvm_g_calc']/bsa
    return c

DERIVED = ['bmi_calc','bsa_m2_calc','waist_hip_ratio_calc','apoa1_apob_ratio_calc','hdl_total_cholesterol_ratio_calc','e_over_eprime_calc','e_over_a_calc','smoking_index_cig_years_calc','alcohol_cumulative_g_day_years_calc','fmd_brachial_pct_calc','nid_brachial_pct_calc','fmd_tibial_pct_calc','nid_tibial_pct_calc','lvm_g_calc','cardiac_index_l_min_m2_calc','lvmi_g_m2_calc']
def recompute(row):
    n, comparators = {}, set()
    for k, v in row.items():
        if k.endswith('_qualifier'):
            if v not in ('', None, '=', '<', '>', '≤', '≥', '<=', '>='): raise ValueError('Unknown measurement qualifier: '+k)
            if v not in ('', None, '='): comparators.add(k[:-10])
        elif v not in ('', None) and not k.endswith('_calc'):
            try:
                x = float(v)
                if math.isfinite(x): n[k] = x
            except (TypeError, ValueError): pass
    return {**{k: row[k] for k in KEYS}, **{k: calculate(n, comparators).get(k, '') for k in DERIVED}}
if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input_csv'); p.add_argument('output_csv'); p.add_argument('--extension', help='Optional unresolved fields, joined by both keys.')
    args = p.parse_args()
    with open(args.input_csv, encoding='utf-8-sig', newline='') as f: rows = list(csv.DictReader(f))
    if args.extension:
        with open(args.extension, encoding='utf-8-sig', newline='') as f: extrows = list(csv.DictReader(f))
        ext = {tuple(r[k] for k in KEYS): r for r in extrows}
        if len(ext) != len(extrows): raise ValueError('Duplicate extension key')
        if set(ext) != {tuple(r[k] for k in KEYS) for r in rows}: raise ValueError('Extension keys differ')
        rows = [{**r, **ext[tuple(r[k] for k in KEYS)]} for r in rows]
    with open(args.output_csv, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=KEYS+DERIVED, lineterminator='\n'); w.writeheader()
        w.writerows(recompute(r) for r in rows)
