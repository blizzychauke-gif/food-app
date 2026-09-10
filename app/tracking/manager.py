from typing import Dict, List
from fastapi import WebSocket
class WSManager:
    def __init__(self): self.active: Dict[str, List[WebSocket]] = {}
    async def connect(self, order_id: str, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(order_id, []).append(ws)
    def disconnect(self, order_id: str, ws: WebSocket):
        if order_id in self.active and ws in self.active[order_id]:
            self.active[order_id].remove(ws)
    async def broadcast(self, order_id: str, msg: dict):
        for ws in list(self.active.get(order_id, [])):
            try: await ws.send_json(msg)
            except: pass
manager = WSManager()