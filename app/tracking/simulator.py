import asyncio
from app.tracking.manager import manager
_tasks={}
async def simulate_driver(order_id: str, polyline: list):
    if order_id in _tasks:
        try: _tasks[order_id].cancel()
        except: pass
    async def run():
        try:
            n=len(polyline)
            for i,pt in enumerate(polyline):
                await manager.broadcast(order_id,{"type":"driver_location_update","order_id":order_id,"lat":pt["lat"],"lng":pt["lng"],"progress":round((i+1)/n*100,1)})
                await asyncio.sleep(1.0)
            from app.store import get_by_id
            o=get_by_id("orders",order_id)
            if o and o["status"]!="DELIVERED":
                o["status"]="DELIVERED"; o["timeline"].append({"status":"DELIVERED"})
            await manager.broadcast(order_id,{"type":"status","order_id":order_id,"status":"DELIVERED"})
        except asyncio.CancelledError: pass
    _tasks[order_id]=asyncio.create_task(run())
    return {"started":True,"points":len(polyline)}