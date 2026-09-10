# Mobile REST + WebSocket Contract

Base: https://api.example.com

## Auth (OTP)
POST /api/auth/otp/send {phone} -> {sent, expires_in, dev_code?(dev only)}
POST /api/auth/otp/verify {phone, code} -> {verified:true}
Errors: 400 No OTP / expired / Incorrect OTP

## Restaurants / Maps
GET /api/restaurants?search= -> [{id,name,cuisine,rating,lat,lng}]
GET /api/restaurants/{id}/menu -> [{id,name,price,image}]
GET /api/maps/autocomplete?query=sandton -> [{name,address,lat,lng}]
POST /api/maps/route {o_lat,o_lng,d_lat,d_lng} -> {distance_km,eta_min,polyline:[{lat,lng}]}

## Orders
POST /api/orders/checkout {customer_id,restaurant_id,items:[{food_id,qty}],address_id?,promo_code?,lat?,lng?}
-> {order:{id,status:PENDING,total,payment_id,...}, payment:{id,checkout_url:/dev/mock-pay/mock_xxx,status:initiated}}
GET /api/orders?customer_id=u1 -> [...]
GET /api/orders/{id} -> order with timeline
POST /api/orders/{id}/status {status: ACCEPTED|PREPARING|READY|ON_THE_WAY|DELIVERED} (restaurant/driver token in prod)

## Payments
POST /api/payments/webhook {payment_id,status:success|failed|cancelled} -> order updated (server-to-server in prod)
GET /api/payments/{id}/verify -> {id,status,amount}
POST /api/payments/{id}/refund

## WebSocket Tracking
URL: wss://api.example.com/ws/orders/{order_id}
Connect -> {"type":"connected","order_id"}
Recv driver: {"type":"driver_location_update","order_id","lat","lng","progress":0-100}
Recv status: {"type":"status","order_id","status":"ON_THE_WAY|DELIVERED"}
Reconnect with backoff, heartbeat every 25s.

## Example flow (Flutter)
1. sendOtp(phone) -> verifyOtp -> store session
2. checkout -> open checkout_url in WebView (mock) or PayFast redirect (real)
3. poll GET /api/orders/{id} until PAID, then open tracking screen
4. open WS, plot polyline + marker, update ETA