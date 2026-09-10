def send_notification(user_id,title,body,role='customer'):
    from app.deps import get_notifs
    return get_notifs().send(user_id,title,body,role)

def recalculate_order(order_id):
    print('Background order recalculation:',order_id)
    return {'order_id':order_id,'ok':True}
