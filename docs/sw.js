// Read with Cinderella offline cache. The version changes whenever the app files change.
const CACHE="cind-f4be5e155c";
const ASSETS=["./", "./fonts/andika-latin-400-normal.woff2", "./fonts/andika-latin-700-normal.woff2", "./fonts/baloo-2-latin-500-normal.woff2", "./fonts/baloo-2-latin-700-normal.woff2", "./fonts/baloo-2-latin-800-normal.woff2", "./icons/apple-touch-icon.png", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png", "./index.html", "./manifest.webmanifest"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{
  const req=e.request;if(req.method!=="GET"||new URL(req.url).origin!==location.origin)return;
  e.respondWith(caches.open(CACHE).then(async c=>{
    const hit=await c.match(req,{ignoreSearch:true});
    const net=fetch(req).then(r=>{if(r&&r.ok)c.put(req,r.clone());return r;}).catch(()=>null);
    return hit||(await net)||c.match("./index.html");
  }));
});
