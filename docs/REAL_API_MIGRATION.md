# REAL_API_MIGRATION - mock -> real without rewriting business logic

Rule: `app/services/*` and `app/api/*` must ONLY import interfaces + factories (`app/deps.py`), never Twilio/PayFast/Google/Firebase/Cloudinary/Resend SDKs.

## 1. OTP: mock=`app/providers/otp/mock.py`, real=`app/providers/otp/twilio.py`
- Env: OTP_PROVIDER=twilio, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SID
- Dashboard: Twilio Console -> Verify -> Create Service -> copy SID
- Switch: OTP_PROVIDER=mock -> twilio, restart
- Test: send to real phone, check Verify logs, test expire/resend/wrong code
- Security: rate-limit send, never return code in prod (Mock returns dev_code only if IS_DEV), store attempts server-side
- No change: routes_auth.py, OrderService

## 2. Payments: mock=`app/providers/payments/mock.py`, real=`app/providers/payments/payfast.py`
- Env: PAYMENT_PROVIDER=payfast, PAYFAST_MERCHANT_ID/KEY/PASSPHRASE, PAYFAST_SANDBOX=true
- Dashboard: PayFast -> Settings -> Integration, set ITN URL https://yourdomain/api/payments/webhook
- Switch: PAYMENT_PROVIDER=mock -> payfast
- Test: sandbox checkout R10, ITN success/fail/cancel/refund, verify signature
- Security: verify ITN signature + amount + server-to-server validation, idempotent webhook
- No change: order checkout/on_payment_success logic

## 3. Maps: mock=`app/providers/maps/mock.py`, real=`app/providers/maps/google_maps.py`
- Env: MAP_PROVIDER=google, GOOGLE_MAPS_API_KEY
- Dashboard: Google Cloud -> Enable Places, Geocoding, Directions, restrict key by bundle ID/IP
- Switch: MAP_PROVIDER=mock -> google
- Test: autocomplete Sandton, geocode, route JHB->Soweto distance/ETA
- Security: key restriction, quota, cache geocodes
- No change: routes_maps, fee calc, simulator (uses RouteInfo.polyline)

## 4. Driver location: `app/tracking/simulator.py` + `manager.py`
- Dev: interpolates mock polyline, broadcasts via WS
- Real: driver app POSTs GPS -> POST /api/orders/{id}/location -> manager.broadcast(driver_location_update). Replace simulator with real GPS, keep WS message shape.

## 5. Push: mock=`app/providers/notifications/mock.py`, real=`app/providers/notifications/firebase.py`
- Env: NOTIFICATION_PROVIDER=firebase, FIREBASE_CREDENTIALS_JSON, FCM device tokens per user
- Dashboard: Firebase Console -> Cloud Messaging, upload APNs key
- Switch: mock -> firebase
- Test: send to test token for customer/restaurant/driver roles
- Security: store tokens per user, don't log tokens
- No change: OrderService notif calls, DB notifications still written

## 6. Storage: mock=`app/providers/storage/mock.py`, real=`app/providers/storage/cloudinary.py`
- Env: STORAGE_PROVIDER=cloudinary, CLOUDINARY_CLOUD_NAME/API_KEY/API_SECRET
- Dashboard: Cloudinary -> Settings -> Upload presets
- Switch: mock -> cloudinary
- Test: upload menu image, check URL
- Security: signed uploads, validate mime/size
- No change: callers use .upload() -> URL string

## 7. Email: mock=`app/providers/email/mock.py`, real=`app/providers/email/resend.py`
- Env: EMAIL_PROVIDER=resend, RESEND_API_KEY, FROM_EMAIL
- Dashboard: Resend -> Domains -> verify DNS, API keys
- Switch: mock -> resend
- Test: send receipt, check inbox/spam, webhook bounces
- Security: SPF/DKIM, don't leak outbox in prod
- No change: service send_email(to,subject,html)

Global prod checklist: APP_ENV=production disables /dev + dev_code + mock-pay page, set CORS origins, HTTPS webhook, secrets manager.