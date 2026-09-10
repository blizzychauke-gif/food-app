from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.store import DB, get_by_id

router = APIRouter(prefix='/api', tags=['customer'])

class ReviewReq(BaseModel):
    customer_id: str
    restaurant_id: str
    stars: int = Field(ge=1, le=5)
    text: str = Field(min_length=2, max_length=500)

@router.get('/customers/{customer_id}')
def customer(customer_id: str):
    c = get_by_id('customers', customer_id)
    if not c: raise HTTPException(404, 'customer not found')
    return c

@router.get('/customers/{customer_id}/addresses')
def addresses(customer_id: str):
    return [a for a in DB['addresses'] if a['customer_id'] == customer_id]

@router.get('/customers/{customer_id}/notifications')
def notifications(customer_id: str):
    return [n for n in DB['notifications'] if n.get('user_id') == customer_id]

@router.get('/promotions')
def promotions():
    return DB['promotions']

@router.get('/promotions/{code}')
def promotion(code: str):
    p = next((x for x in DB['promotions'] if x['code'].upper() == code.upper()), None)
    if not p: raise HTTPException(404, 'promo code not found')
    return p

@router.get('/restaurants/{restaurant_id}/reviews')
def reviews(restaurant_id: str):
    return [r for r in DB['reviews'] if r['restaurant_id'] == restaurant_id]

@router.post('/reviews')
def create_review(r: ReviewReq):
    if not get_by_id('customers', r.customer_id): raise HTTPException(404, 'customer not found')
    if not get_by_id('restaurants', r.restaurant_id): raise HTTPException(404, 'restaurant not found')
    item = {'id': f'rev{len(DB["reviews"])+1}', **r.model_dump()}
    DB['reviews'].append(item)
    return item

@router.get('/admin/summary')
def admin_summary():
    orders = DB['orders']
    delivered = [o for o in orders if o.get('status') == 'DELIVERED']
    revenue = round(sum(o.get('total', 0) for o in delivered), 2)
    avg = round(revenue / len(delivered), 2) if delivered else 0
    return {
        'orders': len(orders), 'delivered_orders': len(delivered), 'revenue': revenue,
        'average_order_value': avg, 'customers': len(DB['customers']),
        'restaurants': len(DB['restaurants']), 'drivers': len(DB['drivers']),
        'pending_orders': len([o for o in orders if o.get('status') in ('PENDING','PAID','ACCEPTED','PREPARING','ON_THE_WAY')]),
    }
