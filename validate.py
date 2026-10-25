"""Validate recomputed measures against an expected CSV, including missingness."""
import argparse, csv, math
from recompute import KEYS, DERIVED, recompute
def read(path):
    with open(path, encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))
def keyed(rows):
    d = {tuple(r[k] for k in KEYS): r for r in rows}
    if len(d) != len(rows): raise ValueError('Duplicate key')
    if any(not all(k) for k in d): raise ValueError('Blank key')
    return d
if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('input_csv');p.add_argument('expected_csv');p.add_argument('--extension');a=p.parse_args()
    observed, expected = keyed(read(a.input_csv)), keyed(read(a.expected_csv))
    if set(observed) != set(expected): raise ValueError('Key mismatch')
    if a.extension:
        ext=keyed(read(a.extension))
        if set(ext)!=set(observed):raise ValueError('Extension key mismatch')
        observed={k:{**r,**ext[k]} for k,r in observed.items()}
    n=0
    for key,r in observed.items():
        calc=recompute(r)
        for f in DERIVED:
            x,y=calc[f],expected[key][f]
            if (x=='')!=(y==''):raise ValueError('Missingness differs: '+f)
            if y!='' and not math.isclose(float(x),float(y),rel_tol=1e-10,abs_tol=1e-10):raise ValueError('Value differs: '+f)
            n+=y!=''
    print(f'Validated {len(observed)} examinations and {n} nonmissing derived values; all keys and missing values match.')
