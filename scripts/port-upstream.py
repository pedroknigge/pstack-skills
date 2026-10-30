# Usage: python3 scripts/port-upstream.py <upstream pstack/skills dir> skills <version>
# Regenerates ps-* leaves from cursor/plugins pstack (MIT, Lauren Tan).
import sys,os,re,shutil,subprocess,json
src,dst,ver=sys.argv[1],sys.argv[2],sys.argv[3]
names=sorted(os.listdir(src),key=len,reverse=True)
alt='|'.join(map(re.escape,names))
pat=re.compile(r'(?<![\w/.-])/('+alt+r')(?![\w-])')
pbt=re.compile(r'`('+alt+r')`')
plk=re.compile(r'\.\./('+alt+r')/')
def xref(t):
  t=pat.sub(lambda m:'/ps-'+m.group(1),t); t=pbt.sub(lambda m:'`ps-'+m.group(1)+'`',t)
  t=re.sub(r'skills/('+alt+r')/',lambda m:'skills/ps-'+m.group(1)+'/',t)
  t=re.sub(r'the ('+alt+r') skill',lambda m:'the ps-'+m.group(1)+' skill',t)
  return plk.sub(lambda m:'../ps-'+m.group(1)+'/',t)
for n in os.listdir(src):
  s=os.path.join(src,n); d=os.path.join(dst,'ps-'+n)
  if os.path.exists(d): shutil.rmtree(d)
  shutil.copytree(s,d)
  for root,_,fs in os.walk(d):
    for f in fs:
      if not f.endswith('.md'): continue
      p=os.path.join(root,f); t=open(p).read()
      if p==os.path.join(d,'SKILL.md'):
        fm,body=t.split('\n---\n',1); fm=fm[4:]
        lines=fm.split('\n'); out=[]
        for l in lines:
          if l.startswith('name:'): out.append('name: ps-'+n); continue
          if l.startswith('description:'):
            v=l[len('description:'):].strip()
            if v.startswith('"'): v=json.loads(v)
            v=xref(v)
            v=f'v{ver}. {v} If the leading version is not the latest in VERSION / changelog, update the skill before using it.'
            out.append('description: '+json.dumps(v,ensure_ascii=False)); out.append('license: MIT'); continue
          out.append(l)
        out+=['metadata:',f'  version: "{ver}"','  author: pedroknigge']
        t='---\n'+'\n'.join(out)+'\n---\n'+xref(body)
      else: t=xref(t)
      open(p,'w').write(t)

# Keep installs lean: upstream statechart test suite + ~4 MB TLC corpus lives in tests/, not skills/.
st=os.path.join(dst,'ps-statechart','scripts','test')
if os.path.isdir(st):
  out=os.path.join(dst,'..','tests','upstream-ps-statechart','test')
  if os.path.exists(out): shutil.rmtree(out)
  os.makedirs(os.path.dirname(out),exist_ok=True); shutil.move(st,out)
