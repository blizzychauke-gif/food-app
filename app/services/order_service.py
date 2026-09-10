import uuid
from app.store import DB, get_by_id, find_orders_by_payment
from app.providers.maps.interface import Coords

class OrderService:
    def __init__(self, payments, maps, notifs, email):
        self.payments=payments; self.maps=maps; self.notifs=notifs; self.email=email

    def checkout(self, customer_id, restaurant_id, items, address_id=None, promo_code=None, lat=None, lng=None):
        cust=get_by_id("customers",customer_id)
        if not cust: raise ValueError("customer not found")
        rest=get_by_id("restaurants",restaurant_id)
        if not rest: raise ValueError("restaurant not found")
        # items: [{food_id, qty}]
        detailed=[]; subtotal=0
        for it in items:
            f=get_by_id("foods",it["food_id"])
            if not f or f["restaurant_id"]!=restaurant_id: raise ValueError(f"invalid food {it['food_id']}")
            qty=int(it.get("qty",1)); subtotal+=f["price"]*qty
            detailed.append({"food_id":f["id"],"name":f["name"],"price":f["price"],"qty":qty})
        discount=0
        if promo_code:
            promo=next((p for p in DB["promotions"] if p["code"]==promo_code),None)
            if promo: discount=round(subtotal*promo["percent"]/100,2)
        # delivery location
        if address_id:
            addr=get_by_id("addresses",address_id)
            if not addr: raise ValueError("address not found")
            clat, clng = addr["lat"], addr["lng"]
            addr_text=addr["address"]
        else:
            clat, clng = lat or -26.1076, lng or 28.0570
            addr_text=self.maps.reverse_geocode(clat,clng)
        # distance fee via maps
        try:
            route=self.maps.route(Coords(rest["lat"],rest["lng"]),Coords(clat,clng))
            fee=round(20+route.distance_km*4,2)
        except: fee=35.0; route=None
        total=round(subtotal-discount+fee,2)
        oid=f"ord_{uuid.uuid4().hex[:8]}"
        driver=DB["drivers"][0] if DB["drivers"] else None
        order={"id":oid,"customer_id":customer_id,"restaurant_id":restaurant_id,
            "items":detailed,"subtotal":round(subtotal,2),"discount":discount,"delivery_fee":fee,"total":total,
            "status":"PENDING","payment_id":None,"driver_id":driver["id"] if driver else None,
            "delivery_address":addr_text,"customer_lat":clat,"customer_lng":clng,
            "restaurant_lat":rest["lat"],"restaurant_lng":rest["lng"],
            "timeline":[{"status":"PENDING"}]}
        DB["orders"].append(order)
        pi=self.payments.create_payment(oid,total)
        order["payment_id"]=pi.id
        return order, pi

    def on_payment_success(self, payment_id):
        o=find_orders_by_payment(payment_id)
        if not o: raise ValueError("order not found for payment")
        o["status"]="PAID"; o["timeline"].append({"status":"PAID"})
        self.notifs.send(o["restaurant_id"],"New Order!",f"Order {o['id']} PAID R{o['total']}",role="restaurant")
        self.notifs.send(o["customer_id"],"Payment success",f"Order {o['id']} confirmed",role="customer")
        cust=get_by_id("customers",o["customer_id"])
        if cust: self.email.send_email(cust["email"],"Receipt",f"Paid R{o['total']} for {o['id']}")
        return o

    def on_payment_failed(self, payment_id):
        o=find_orders_by_payment(payment_id)
        if not o: raise ValueError("order not found")
        o["status"]="PAYMENT_FAILED"; o["timeline"].append({"status":"PAYMENT_FAILED"})
        self.notifs.send(o["customer_id"],"Payment failed",f"Order {o['id']} failed",role="customer")
        return o

    def update_status(self, order_id, new_status):
        o=get_by_id("orders",order_id)
        if not o: raise ValueError("order not found")
        o["status"]=new_status; o["timeline"].append({"status":new_status})
        if new_status=="ACCEPTED":
            self.notifs.send(o["customer_id"],"Restaurant accepted",f"{o['id']} being prepared",role="customer")
        elif new_status=="PREPARING":
            self.notifs.send(o["customer_id"],"Preparing",f"{o['id']} in kitchen",role="customer")
        elif new_status in ("READY","PICKED_UP","ON_THE_WAY"):
            self.notifs.send(o["customer_id"],f"Order {new_status}",f"Driver on way: {o['id']}",role="customer")
            if o.get("driver_id"):
                self.notifs.send(o["driver_id"],"Pickup",f"Deliver {o['id']}",role="driver")
        elif new_status=="DELIVERED":
            self.notifs.send(o["customer_id"],"Delivered","Enjoy!",role="customer")
        return o