# FoodDash — Professional Food Delivery Demo

A full-stack FastAPI + responsive web food-delivery platform. It runs locally without Node/npm and uses mock providers for payments, OTP, maps, notifications and email.

## What is included
- Customer ordering experience with restaurant discovery, search, cuisine filters and menus
- Cart, promo codes, delivery fee calculation and checkout
- Order history, profile, addresses and notifications
- Order lifecycle simulation: paid → accepted → preparing → on the way → delivered
- Live-style driver tracking UI + WebSocket backend
- Restaurant reviews
- Operations/admin dashboard at `/admin`
- API health/provider monitoring and Swagger docs at `/docs`
- PWA manifest + offline shell service worker
- Modular provider architecture ready for real PayFast/Twilio/Google Maps/Firebase/Cloudinary/Resend integrations

## Run on Windows PowerShell
```powershell
cd C:\Users\blizz\Downloads\CODING\food-delivery
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:
- Customer app: http://127.0.0.1:8000/
- Operations dashboard: http://127.0.0.1:8000/admin
- Swagger API: http://127.0.0.1:8000/docs
- Developer simulator: http://127.0.0.1:8000/dev

## Demo notes
The database is intentionally in-memory for this demo, so restarting the server resets orders. Real production deployment should replace the store with PostgreSQL/Redis, add authentication/JWT, background jobs, object storage, real payment webhooks, observability and deployment secrets.
