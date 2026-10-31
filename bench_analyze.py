import json, glob, os, re

OUT = '/tmp/bench'
models = [l.strip() for l in open('bench_models.txt') if l.strip()]

def parse(model, tag):
    safe = model.replace('/', '_')
    f = f'{OUT}/{safe}.{tag}.jsonl'
    meta = f'{OUT}/{safe}.{tag}.meta'
    if not os.path.exists(meta):
        return None
    rc, wall = open(meta).read().split()[:2]
    wall = float(wall)
    text = ''
    tok_out = tok_rea = 0
    ts = []
    err = ''
    try:
        for line in open(f, encoding='utf-8', errors='replace'):
            line = line.strip().lstrip('\x1b[0m')
            if not line.startswith('{'):
                m = re.search(r'(\{.*\})', line)
                if not m:
                    if 'Error' in line or 'error' in line: err += line + ' '
                    continue
                line = m.group(1)
            try: d = json.loads(line)
            except: continue
            if 'timestamp' in d: ts.append(d['timestamp'])
            t = d.get('type','')
            p = d.get('part',{})
            if t in ('text','step_start','step_finish'):
                pt = p.get('type','')
                if pt == 'text' and p.get('text'): text += p['text']
                tk = p.get('tokens')
                if tk:
                    tok_out = max(tok_out, tk.get('output',0))
                    tok_rea = max(tok_rea, tk.get('reasoning',0))
            if t == 'error' or 'error' in d and t=='':
                err += json.dumps(d)[:200]
    except Exception as e:
        err += f'PARSE:{e}'
    gen_s = (max(ts)-min(ts))/1000 if len(ts)>=2 else 0
    return dict(rc=rc, wall=wall, text=text, out=tok_out, rea=tok_rea,
                gen_s=gen_s, err=err.strip()[:150])

def grade(text):
    if not text: return '-'
    m = re.search(r'最终答案[：:](.*)', text)
    ans = m.group(1) if m else text[-300:]
    a1 = bool(re.search(r'3415\s*/\s*512|6\.6[67]\d*|6\.7\b|≈\s*6\.67', ans))
    seg = ans
    others = re.findall(r'[BCDE]', seg)
    a2 = 'A' in seg and not others
    a3 = '385' in seg
    return f"{int(a1)}{int(a2)}{int(a3)}"

print(f"{'model':44s} {'grade':5s} {'out_tok':>7s} {'rea_tok':>7s} {'gen_s':>6s} {'tok/s':>6s} {'wall':>6s} {'spd_tps':>7s}  err")
for model in models:
    i = parse(model, 'intel')
    s = parse(model, 'speed')
    if i is None: print(f"{model:44s} NODATA"); continue
    tps = round((i['out']+i['rea'])/i['gen_s'],1) if i['gen_s']>0 and (i['out']+i['rea'])>0 else 0
    stps = ''
    if s and s['gen_s']>0 and s['out']>0:
        stps = round(s['out']/s['gen_s'],1)
    err = i['err'] or (s['err'] if s else '')
    g = grade(i['text'])
    print(f"{model:44s} {g:5s} {i['out']:7d} {i['rea']:7d} {i['gen_s']:6.1f} {tps:6} {i['wall']:6.1f} {stps!s:>7s}  {err}")
