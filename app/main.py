from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from app.config import settings, provider_status
from app.seed import seed_db
from app.api.routes_auth import router as auth_r
from app.api.routes_restaurants import router as rest_r
from app.api.routes_maps import router as maps_r
from app.api.routes_orders import router as orders_r
from app.api.routes_payments import router as pay_r
from app.api.routes_dev import router as dev_r
from app.api.routes_customer import router as customer_r
from app.api.routes_auth_prod import router as auth_prod_r
from app.api.routes_admin import router as admin_r
from app.api.routes_restaurant_portal import router as restaurant_portal_r
from app.api.routes_driver import router as driver_r
from app.api.routes_payfast import router as payfast_r
from app.production import init_db
from app.tracking.manager import manager

app=FastAPI(title="FoodDash Delivery Platform", version="2.0.0", description="Professional food ordering, delivery and operations API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
seed_db()
init_db()
app.include_router(auth_r); app.include_router(auth_prod_r); app.include_router(rest_r); app.include_router(maps_r)
app.include_router(admin_r); app.include_router(restaurant_portal_r); app.include_router(driver_r); app.include_router(payfast_r)
app.include_router(orders_r); app.include_router(pay_r); app.include_router(dev_r); app.include_router(customer_r)

@app.get("/", response_class=HTMLResponse)
def home():
    from pathlib import Path
    return Path("app/static/index.html").read_text(encoding="utf-8")

@app.get("/api/providers")
def prov(): return provider_status()

@app.get("/api/health")
def health():
    return {"status":"ok","service":"fooddash","version":"3.0.0","mode":"mock" if settings.IS_DEV else "production"}

@app.websocket("/ws/orders/{order_id}")
async def ws_order(ws: WebSocket, order_id: str):
    await manager.connect(order_id,ws)
    try:
        await ws.send_json({"type":"connected","order_id":order_id})
        while True: await ws.receive_text()
    except WebSocketDisconnect: manager.disconnect(order_id,ws)

@app.get("/dev/mock-pay/{pid}",response_class=HTMLResponse)
def mock_pay(pid: str):
    if not settings.IS_DEV: raise HTTPException(404)
    return f"""<html><body style="font-family:sans-serif;padding:30px">
    <h2>MOCK PayFast - {pid}</h2>
    <p>Simulated checkout. No real money.</p>
    <button onclick="fetch('/api/dev/simulate/payment-success?payment_id={pid}',{{method:'POST'}}).then(r=>r.json()).then(j=>document.body.innerHTML='<pre>SUCCESS '+JSON.stringify(j,null,2)+'</pre>')">Pay SUCCESS</button>
    <button onclick="fetch('/api/dev/simulate/payment-failed?payment_id={pid}',{{method:'POST'}}).then(r=>r.json()).then(j=>document.body.innerHTML='<pre>FAILED '+JSON.stringify(j,null,2)+'</pre>')">Pay FAIL</button>
    </body></html>"""

@app.get("/login", response_class=HTMLResponse)
def login_page(): return FileResponse("app/static/portal/login.html")

@app.get("/restaurant", response_class=HTMLResponse)
def restaurant_page(): return FileResponse("app/static/portal/restaurant.html")

@app.get("/driver", response_class=HTMLResponse)
def driver_page(): return FileResponse("app/static/portal/driver.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    return FileResponse("app/static/admin.html")

@app.get("/dev",response_class=HTMLResponse)
def dev_page():
    if not settings.IS_DEV: raise HTTPException(404)
    return """<html><head><title>DEV Dashboard</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>body{font-family:sans-serif;padding:20px;max-width:1000px;margin:auto}button{margin:4px;padding:8px 12px}.badge{background:#111;color:#0f0;padding:4px 8px;border-radius:6px;margin:2px;display:inline-block}#map{height:320px;margin-top:12px}pre{background:#111;color:#0f0;padding:10px;overflow:auto;max-height:240px}</style>
</head><body>
<h1>DEV Dashboard (MOCK ONLY)</h1><div id="prov"></div>
<h3>Simulate</h3>
OrderID <input id="oid" placeholder="ord_xxx" style="width:200px"/> PaymentID <input id="pid" placeholder="mock_xxx" style="width:200px"/>
<br/>
<button onclick="call('/api/dev/simulate/payment-success?payment_id='+v('pid'))">Payment Success</button>
<button onclick="call('/api/dev/simulate/payment-failed?payment_id='+v('pid'))">Payment Failed</button>
<button onclick="call('/api/dev/simulate/restaurant-accept?order_id='+v('oid'))">Restaurant Accept</button>
<button onclick="call('/api/dev/simulate/preparation?order_id='+v('oid'))">Preparation</button>
<button onclick="call('/api/dev/simulate/delivery?order_id='+v('oid'))">Delivery + Driver Move</button>
<button onclick="call('/api/dev/simulate/driver-movement?order_id='+v('oid'))">Driver Movement Only</button>
<button onclick="call('/api/dev/simulate/test-notification?user_id=u1&role=customer')">Test Notification</button>
<button onclick="connectWS()">Connect Driver WS</button>
<div id="map"></div><h3>Output</h3><pre id="out">ready...</pre>
<h3>OTP Logs</h3><pre id="otp"></pre><h3>Notifications</h3><pre id="notif"></pre>
<script>
function v(id){return document.getElementById(id).value}
async function call(u){let r=await fetch(u,{method:'POST'});document.getElementById('out').textContent=JSON.stringify(await r.json(),null,2);refresh()}
async function refresh(){
 let p=await (await fetch('/api/dev/providers')).json();
 document.getElementById('prov').innerHTML=Object.entries(p).map(([k,val])=>'<span class=badge>'+k+': '+val+'</span>').join('');
 try{document.getElementById('otp').textContent=JSON.stringify(await (await fetch('/api/dev/otp-logs')).json(),null,2)}catch(e){}
 try{document.getElementById('notif').textContent=JSON.stringify(await (await fetch('/api/dev/notifications')).json(),null,2)}catch(e){}
}
var map=L.map('map').setView([-26.1076,28.057],11);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);
var marker=null;var ws=null;
function connectWS(){let oid=v('oid');if(!oid){alert('enter order id');return}
 ws=new WebSocket((location.protocol=='https:'?'wss://':'ws://')+location.host+'/ws/orders/'+oid);
 ws.onmessage=e=>{let m=JSON.parse(e.data);document.getElementById('out').textContent=JSON.stringify(m,null,2);
  if(m.lat){if(!marker)marker=L.marker([m.lat,m.lng]).addTo(map);else marker.setLatLng([m.lat,m.lng]);map.setView([m.lat,m.lng],13)}}}
refresh();setInterval(refresh,5000);
</script></body></html>"""