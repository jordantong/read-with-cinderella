#!/usr/bin/env python3
"""Build the installable iPad app (../docs) from read-with-cinderella.html.
Run from anywhere:  python3 build.py"""
import re, json, shutil, os, hashlib
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'read-with-cinderella.html'); OUT=os.path.join(os.path.dirname(HERE),'docs')
os.makedirs(OUT,exist_ok=True)  # files are overwritten in place (no deletes)
shutil.copytree(os.path.join(HERE,'fonts'),os.path.join(OUT,'fonts'),dirs_exist_ok=True)
shutil.copytree(os.path.join(HERE,'icons'),os.path.join(OUT,'icons'),dirs_exist_ok=True)
src=open(SRC,encoding='utf-8').read()
src=re.sub(r'<link rel="preconnect"[^>]*>\n?','',src)
src=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?','',src)
head,body=src.split('</style>',1); head+='</style>'
FONTS=[('Andika','andika-latin-400-normal.woff2',400),('Andika','andika-latin-700-normal.woff2',700),
       ('Baloo 2','baloo-2-latin-500-normal.woff2',500),('Baloo 2','baloo-2-latin-700-normal.woff2',700),('Baloo 2','baloo-2-latin-800-normal.woff2',800)]
ff=''.join(f'@font-face{{font-family:"{fam}";font-style:normal;font-weight:{w};font-display:swap;src:url(fonts/{f}) format("woff2")}}\n' for fam,f,w in FONTS)
BG="#F7F1FF"
page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Cinderella">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="{BG}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<style>
{ff}html{{height:100%;background:{BG};overscroll-behavior:none}}
body{{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);overscroll-behavior:none;-webkit-text-size-adjust:100%}}
</style>
{head}
</head>
<body>
{body}
<script>if("serviceWorker" in navigator)window.addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{{}}));</script>
</body>
</html>
'''
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(page)
json.dump({"name":"Read with Cinderella","short_name":"Cinderella","description":"Learning to read with Cinderella the unicorn","start_url":"./","scope":"./","display":"standalone","orientation":"any",
  "background_color":BG,"theme_color":BG,
  "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png"},
           {"src":"icons/icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},
  open(os.path.join(OUT,'manifest.webmanifest'),'w'),indent=2)
files=sorted(os.path.relpath(os.path.join(r,f),OUT) for r,_,fs in os.walk(OUT) for f in fs if not f.startswith('.') and f not in ('sw.js','README.txt'))
h=hashlib.sha1(b''.join(open(os.path.join(OUT,f),'rb').read() for f in files)).hexdigest()[:10]
assets=['./']+['./'+f.replace(os.sep,'/') for f in files]
open(os.path.join(OUT,'sw.js'),'w').write(f'''// Read with Cinderella offline cache. The version changes whenever the app files change.
const CACHE="cind-{h}";
const ASSETS={json.dumps(assets)};
self.addEventListener("install",e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));}});
self.addEventListener("fetch",e=>{{
  const req=e.request;if(req.method!=="GET"||new URL(req.url).origin!==location.origin)return;
  e.respondWith(caches.open(CACHE).then(async c=>{{
    const hit=await c.match(req,{{ignoreSearch:true}});
    const net=fetch(req).then(r=>{{if(r&&r.ok)c.put(req,r.clone());return r;}}).catch(()=>null);
    return hit||(await net)||c.match("./index.html");
  }}));
}});
''')
shutil.copy(os.path.join(HERE,'app-README.txt'),os.path.join(OUT,'README.txt'))
print('Built docs/ (cache version cind-%s, %d files)'%(h,len(files)))
