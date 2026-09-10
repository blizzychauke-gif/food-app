# Production deployment

## 1. Server
Use an Ubuntu 22.04/24.04 VPS with Docker and a domain pointing to the server.

## 2. Configure secrets
Copy `.env.example` to `.env` and replace the JWT secret, PayFast credentials, Google Maps key, Twilio credentials and public URLs.

Generate a strong JWT secret with:
`python -c "import secrets; print(secrets.token_urlsafe(48))"`

## 3. Start
`docker compose up -d --build`

The API is on port 8000. Put Nginx/Cloudflare in front and enable HTTPS. WebSockets must be proxied for `/ws/`.

## 4. PayFast
Set `PAYMENT_PROVIDER=payfast` and use sandbox first. Register the ITN URL as `/api/payments/payfast/itn`. Move to `PAYFAST_MODE=live` only after a successful sandbox test.

## 5. Google Maps
Enable Maps Platform APIs required by your usage (Directions, Geocoding and Places) and restrict the key by API and server origin where applicable.

## 6. Operations
- Customer: `/`
- Login: `/login`
- Restaurant: `/restaurant`
- Driver: `/driver`
- Admin: `/admin`
- Swagger: `/docs`

The initial development admin is `admin@fooddash.local` / `ChangeMe123!`; change/remove it immediately in production.
