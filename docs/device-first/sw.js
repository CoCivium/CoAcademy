/* CoDevice R0: user-click installation only, same-origin public shell; no user data. */
const CACHE="cocivium-device-first-r0-20261024";
const SHELL=["./","./index.html","./manifest.json","./icon.svg"];
self.addEventListener("install",e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(a=>Promise.all(a.filter(k=>k.startsWith("cocivium-device-first-")&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{
const r=e.request;
if(r.method!=="GET"||new URL(r.url).origin!==self.location.origin)return;
if(r.mode==="navigate"){e.respondWith(fetch(r).catch(()=>caches.match("./index.html")));return;}
e.respondWith(caches.match(r).then(hit=>hit||fetch(r)));
});
