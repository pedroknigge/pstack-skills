# Usage: python3 scripts/port-upstream.py <upstream pstack/skills dir> skills <version>
# Regenerates ps-* leaves from cursor/plugins pstack (MIT, Lauren Tan).
import sys,os,re,shutil,subprocess,json
src,dst,ver=sys.argv[1],sys.argv[2],sys.argv[3]
names=sorted(os.listdir(src),key=len,reverse=True)
alt='|'.join(map(re.escape,names))
shorts=sorted((n[len('principle-'):] for n in names if n.startswith('principle-') and n[len('principle-'):] not in names),key=len,reverse=True)
salt='|'.join(map(re.escape,shorts))
pat=re.compile(r'(?<![\w/.-])/('+alt+r')(?![\w-])')
pbt=re.compile(r'`('+alt+r')`')
pbold=re.compile(r'\*\*('+alt+r')\*\*')
pshort=re.compile(r'\*\*('+salt+r')\*\*') if salt else None
pplus=re.compile(r'(?<![\w-])\+ ('+alt+r')(?![\w-])')
pverb=re.compile(r'(?i)(?<![A-Za-z0-9_-])(run|use) ('+alt+r')(?![\w-])')
pthe=re.compile(r'(?<![\w-])the ('+alt+r') skill')
plk=re.compile(r'\.\./('+alt+r')/')
pdocs=re.compile(r'(?:\.\./)+docs/(guide|harness)/([\w.-]+)')
def xref(t):
  t=pdocs.sub(lambda m:'https://github.com/cursor/plugins/tree/main/pstack/docs/'+m.group(1)+'/'+m.group(2),t)
  t=pat.sub(lambda m:'/ps-'+m.group(1),t); t=pbt.sub(lambda m:'`ps-'+m.group(1)+'`',t)
  t=pbold.sub(lambda m:'**ps-'+m.group(1)+'**',t)
  if pshort: t=pshort.sub(lambda m:'**ps-principle-'+m.group(1)+'**',t)
  t=pplus.sub(lambda m:'+ ps-'+m.group(1),t)
  t=pverb.sub(lambda m:m.group(1)+' ps-'+m.group(2),t)
  t=pthe.sub(lambda m:'the ps-'+m.group(1)+' skill',t)
  t=re.sub(r'skills/('+alt+r')/',lambda m:'skills/ps-'+m.group(1)+'/',t)
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
        lines=fm.split('\n'); out=[]; i=0
        while i<len(lines):
          l=lines[i]
          if l.startswith('name:'): out.append('name: ps-'+n); i+=1; continue
          if l.startswith('description:'):
            v=l[len('description:'):].strip()
            if v in ('>','>-','|','|-'):
              i+=1; parts=[]
              while i<len(lines) and (lines[i].startswith((' ','\t')) or (lines[i].strip()=='' and i+1<len(lines) and lines[i+1].startswith((' ','\t')))):
                if lines[i].strip(): parts.append(lines[i].strip())
                i+=1
              v=' '.join(parts)
            else:
              if v.startswith('"'): v=json.loads(v)
              i+=1
            v=xref(v)
            v=f'v{ver}. {v} If the leading version is not the latest in VERSION / changelog, update the skill before using it.'
            out.append('description: '+json.dumps(v,ensure_ascii=False)); out.append('license: MIT'); continue
          out.append(l); i+=1
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
rc=subprocess.run([sys.executable,os.path.join(os.path.dirname(os.path.abspath(__file__)),'check-pack.py')]).returncode
if rc: sys.exit(rc)
