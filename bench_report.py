import json, glob, os, re, html, datetime

OUT='/tmp/bench'
DEST='/mnt/c/Users/22448/opencode-bench'
os.makedirs(DEST, exist_ok=True)
models=[l.strip() for l in open('/mnt/c/Users/22448/bench_models.txt') if l.strip()]

QUOTA={
 'iceman-contributor-free':'∞ 限时','beam-free':'∞ 限时(区域锁)','deepseek-v4.1-flash':'$100',
 'glm-5.3-flash':'$60','glm-5.2':'$60','kimi-k2.7-code':'$60','longcat-2.0':'$60',
 'mimo-v2.6-flash':'$60','mimo-v2.5':'$60','minimax-m3':'$60','qwen3.7-plus':'$60','hy3':'$60',
 'muse-spark-1.3-contributor':'$60(区域锁)','muse-spark-1.2-contributor':'$60(区域锁)',
 'gemini-4-argon':'$30','qwen3.8-flash':'$30','hy4-preview':'$30','minimax-m3.1-flash':'$20',
 'glm-5.3':'$15','kimi-k3.1-pro':'$15','kimi-k3':'$15','gpt-6-luna':'$15(区域锁)',
 'gpt-5.6-luna':'$15(区域锁)','claude-haiku-5-5':'$15','qwen3.8-max':'$15','grok-4.7':'$15',
 'step-5-preview':'$15','deepseek-v4-pro':'$15','mimo-v2.6-pro':'$15','mimo-v2.5-pro':'$15',
 'deepseek-v4.1-flash-free':'Zen试用','glm-5.3-flash-free':'Zen试用','mimo-v2.6-flash-free':'Zen试用',
 'flint-40b-free':'Zen试用','nemotron-3.5-lightning-free':'Zen试用',
 'nemotron-3.5-super-vl-free':'Zen试用','big-pickle':'Zen试用','gpt-6-astra':'LAN relay'}

def parse(model,tag):
    safe=model.replace('/','_')
    f=f'{OUT}/{safe}.{tag}.jsonl'; mt=f'{OUT}/{safe}.{tag}.meta'
    if not os.path.exists(mt): return None
    parts=open(mt).read().split(); rc,wall=parts[0],float(parts[1])
    text='';out=rea=0;err=''
    for line in open(f,encoding='utf-8',errors='replace'):
        line=line.strip()
        if not line.startswith('{'):continue
        try:d=json.loads(line)
        except:continue
        p=d.get('part',{})
        if p.get('type')=='text':text+=p.get('text','')
        tk=p.get('tokens')
        if tk:out=max(out,tk.get('output',0));rea=max(rea,tk.get('reasoning',0))
        if d.get('type')=='error':err=d['error'].get('data',{}).get('message','')[:120]
    return dict(wall=wall,text=text,out=out,rea=rea,err=err)

def grade_q(text):
    if not text:return (None,None,None),''
    m=re.search(r'最终答案[：:](.*)',text)
    ans=m.group(1) if m else text[-300:]
    a1=bool(re.search(r'3415\s*/\s*512|6830\s*/\s*1024|6\.669|6\.67\b|10245\s*/\s*1536',ans))
    a2='A' in ans and not re.findall(r'[BCDE]',ans)
    a3='385' in ans
    return (a1,a2,a3),ans.strip()[:120]

rows=[]
for m in models:
    name=m.split('/',1)[1]; tier=m.split('/',1)[0]
    i=parse(m,'intel');s=parse(m,'speed')
    r=dict(model=m,name=name,tier=tier,quota=QUOTA.get(name,'-'))
    if i is None:r['status']='nodata';rows.append(r);continue
    (a1,a2,a3),ans=grade_q(i['text'])
    r.update(iwall=i['wall'],iout=i['out'],irea=i['rea'],ierr=i['err'],
             q1=a1,q2=a2,q3=a3,ansline=ans)
    if i['err']:r['status']='error';r['errmsg']=i['err']
    elif a1 is None:r['status']='fail'
    else:r['status']='ok';r['score']=int(a1)+int(a2)+int(a3)
    if s and not s['err'] and s['out']>0:
        r['swall']=s['wall'];r['sout']=s['out']
        r['tps']=round(s['out']/max(s['wall']-3.0,0.5))
    elif s and s['err']:r.setdefault('serr',s['err'][:60])
    rows.append(r)

json.dump(rows,open(f'{DEST}/results.json','w'),ensure_ascii=False,indent=1)

QHTML='''<b>题1（递推）</b> A缸10升水B缸空；每步把A一半倒入B、再把B一半倒回A，5次后A=？ 〔正确: 3415/512 ≈ 6.670〕<br>
<b>题2（真假话）</b> A:"B,C同类" B:"D,E不同类" C:"A说谎" D:"B诚实" E:"C,D不同类"，问谁诚实 〔正确: 仅A〕<br>
<b>题3（计数）</b> lcm(a,b)=2³·3⁵·5² 的有序正整数对数 〔正确: 385〕'''

def esc(x):return html.escape(str(x))
def tick(v):
    if v is True:return '<td class="p">✓</td>'
    if v is False:return '<td class="f">✗</td>'
    return '<td class="na">—</td>'

trs=[]
for r in sorted(rows,key=lambda x:(x.get('status')!='ok',-(x.get('score') or 0),x.get('swall',999))):
    if r['status']=='ok':
        score=f"{r['score']}/3"
        spd=f"{r.get('swall',0):.1f}s" if 'swall' in r else '—'
        tps=f"~{r['tps']}" if 'tps' in r else '—'
        rea=f"{r['irea']}"
        note=''
        if r['name']=='iceman-contributor-free':note='当前默认 · 唯一无限免费'
        elif r['name']=='deepseek-v4.1-flash':note='订阅内最强全能（$100额度）'
        elif r['name']=='minimax-m3':note='最快档，适合高频agent'
        elif r['name']=='longcat-2.0':note='定速任务输出异常'
        elif 'free' in r['name'] or r['name']=='big-pickle':note='Zen试用配额~1-3次/17h'
        trs.append(f"<tr><td class=m>{esc(r['name'])}</td><td>{esc(r['tier'])}</td><td>{esc(r['quota'])}</td>{tick(r['q1'])}{tick(r['q2'])}{tick(r['q3'])}<td class=p>{score}</td><td>{spd}</td><td>{tps}</td><td>{r['iout']}</td><td>{rea}</td><td class=n>{esc(note)}</td></tr>")
    else:
        msg=r.get('errmsg') or 'fail'
        trs.append(f"<tr class=bad><td class=m>{esc(r['name'])}</td><td>{esc(r['tier'])}</td><td>{esc(r['quota'])}</td><td colspan=3 class=na>{'✗' if r['status']=='fail' else '—'}</td><td class=f>{'0/3' if r['status']=='fail' else 'ERR'}</td><td>{r.get('swall','—') if isinstance(r.get('swall'),str) else (format(r.get('swall'),'.1f')+'s' if 'swall' in r else '—')}</td><td>—</td><td>{r.get('iout',0)}</td><td>{r.get('irea',0)}</td><td class=n>{esc(msg)}</td></tr>")

HTML=f'''<!DOCTYPE html><html lang=zh><head><meta charset=utf-8>
<title>OpenCode 模型实测对比 2026-10-31</title>
<style>
body{{font-family:system-ui,"Segoe UI",sans-serif;margin:24px;background:#0d1117;color:#c9d1d9}}
h1{{font-size:20px}} .meta{{color:#8b949e;font-size:13px;margin-bottom:16px}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #30363d;padding:5px 9px;text-align:left;white-space:nowrap}}
th{{background:#161b22;position:sticky;top:0}} td.m{{font-family:Consolas,monospace;color:#79c0ff}}
td.p{{color:#3fb950;font-weight:700}} td.f{{color:#f85149;font-weight:700}} td.na{{color:#8b949e}}
td.n{{white-space:normal;color:#8b949e;font-size:12px}} tr.bad td{{background:#1c1313}}
.q{{background:#161b22;border:1px solid #30363d;padding:12px;margin:12px 0;font-size:13px;line-height:1.7}}
h2{{font-size:15px;color:#79c0ff}}
</style></head><body>
<h1>OpenCode 模型实测对比 <span class=meta>2026-10-31 · 37 模型 · 订阅: Go $10/月</span></h1>
<div class=q>{QHTML}</div>
<div class=meta>测速 = 定速任务（输出1~100，~200 token）端到端耗时，含 ~3s 客户端启动；~TPS 为估算值。Zen 试用模型约 1~3 次/17h 每模型。</div>
<table><tr><th>模型</th><th>层级</th><th>月额度</th><th>题1</th><th>题2</th><th>题3</th><th>得分</th><th>定速耗时</th><th>~TPS</th><th>输出tok</th><th>推理tok</th><th>备注</th></tr>
{''.join(trs)}
</table>
<h2>结论</h2>
<ul>
<li><b>日常默认</b>: iceman-contributor-free — 唯一无限免费 + 3/3 + 中速</li>
<li><b>主力升级</b>: deepseek-v4.1-flash — $100/月额度全场最大 + 3/3 + 快</li>
<li><b>高频 agent</b>: minimax-m3 — 最快 + 3/3 + $60</li>
<li><b>硬骨头</b>: glm-5.3 / kimi-k3.1-pro / qwen3.8-max / gemini-4-argon（全对，$15-30 小额度）</li>
<li><b>尝鲜</b>: Zen free 八件套；注意 mimo-v2.6-flash-free 智力掉档、nemotron-super-vl 极慢</li>
<li><b>不可用</b>: gpt-luna×2 / muse-spark×2 / beam×2 区域锁；mimo-v2.5×2 已弃用；LAN relay 离线</li>
</ul></body></html>'''
open(f'{DEST}/report.html','w',encoding='utf-8').write(HTML)
print('wrote',f'{DEST}/report.html','rows:',len(rows))
ok=[r for r in rows if r['status']=='ok']
print('passed 3/3:',sum(1 for r in ok if r['score']==3),'of',len(ok),'ok;',sum(1 for r in rows if r['status']!='ok'),'not ok')
