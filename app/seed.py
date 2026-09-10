from app.store import DB

def seed_db():
    for k in DB: DB[k].clear()

    DB["restaurants"] = [
        {"id":"r1","name":"Bunny Chow House","cuisine":"Durban Curry","rating":4.7,"lat":-29.8587,"lng":31.0218,"address":"45 Florida Rd, Durban","image":"https://picsum.photos/seed/bunny/600/400"},
        {"id":"r2","name":"Braam Burger Co","cuisine":"Burgers","rating":4.5,"lat":-26.1929,"lng":28.0340,"address":"70 Jorissen St, Braamfontein, JHB","image":"https://picsum.photos/seed/burger/600/400"},
        {"id":"r3","name":"Cape Malay Kitchen","cuisine":"Cape Malay","rating":4.8,"lat":-33.9249,"lng":18.4241,"address":"12 Long St, Cape Town","image":"https://picsum.photos/seed/capemalay/600/400"},
        {"id":"r4","name":"Sushi Sandton","cuisine":"Sushi","rating":4.6,"lat":-26.1076,"lng":28.0570,"address":"Sandton City, Sandton, JHB","image":"https://picsum.photos/seed/sushi/600/400"},
    ]
    DB["categories"] = [
        {"id":"c1","name":"Mains"},{"id":"c2","name":"Starters"},
        {"id":"c3","name":"Desserts"},{"id":"c4","name":"Drinks"},{"id":"c5","name":"Sushi"},
    ]
    DB["foods"] = [
        {"id":"f1","restaurant_id":"r1","category_id":"c1","name":"Chicken Bunny Chow","price":89.0,"image":"https://picsum.photos/seed/f1/600/400","desc":"Quarter loaf, Durban curry"},
        {"id":"f2","restaurant_id":"r1","category_id":"c1","name":"Beef Bunny Chow","price":99.0,"image":"https://picsum.photos/seed/f2/600/400","desc":"Slow cooked beef"},
        {"id":"f3","restaurant_id":"r2","category_id":"c1","name":"Boerewors Roll","price":65.0,"image":"https://picsum.photos/seed/f3/600/400","desc":"Farm boerie, caramelised onion"},
        {"id":"f4","restaurant_id":"r2","category_id":"c1","name":"Smash Burger","price":110.0,"image":"https://picsum.photos/seed/f4/600/400","desc":"Double smash, cheddar"},
        {"id":"f5","restaurant_id":"r2","category_id":"c2","name":"Loaded Fries","price":55.0,"image":"https://picsum.photos/seed/f5/600/400","desc":"Cheese sauce, jalapeno"},
        {"id":"f6","restaurant_id":"r3","category_id":"c1","name":"Bobotie","price":115.0,"image":"https://picsum.photos/seed/f6/600/400","desc":"Cape Malay classic, yellow rice"},
        {"id":"f7","restaurant_id":"r3","category_id":"c1","name":"Chicken Biryani","price":120.0,"image":"https://picsum.photos/seed/f7/600/400","desc":"Saffron rice, raita"},
        {"id":"f8","restaurant_id":"r3","category_id":"c3","name":"Malva Pudding","price":60.0,"image":"https://picsum.photos/seed/f8/600/400","desc":"Apricot, custard"},
        {"id":"f9","restaurant_id":"r4","category_id":"c5","name":"Sushi Platter 24pc","price":249.0,"image":"https://picsum.photos/seed/f9/600/400","desc":"Salmon, tuna, california"},
        {"id":"f10","restaurant_id":"r4","category_id":"c5","name":"Salmon Roses","price":149.0,"image":"https://picsum.photos/seed/f10/600/400","desc":"8pc salmon roses"},
        {"id":"f11","restaurant_id":"r1","category_id":"c4","name":"Mango Lassi","price":35.0,"image":"https://picsum.photos/seed/f11/600/400","desc":"Fresh mango, yoghurt"},
        {"id":"f12","restaurant_id":"r2","category_id":"c4","name":"Craft Cola 500ml","price":30.0,"image":"https://picsum.photos/seed/f12/600/400","desc":"Local craft cola"},
    ]
    DB["customers"] = [
        {"id":"u1","name":"Thabo M","phone":"+27821234567","email":"thabo@demo.co.za"},
        {"id":"u2","name":"Lerato K","phone":"+27829876543","email":"lerato@demo.co.za"},
        {"id":"u3","name":"Pieter V","phone":"+27835551234","email":"pieter@demo.co.za"},
    ]
    DB["drivers"] = [
        {"id":"d1","name":"Sipho D","phone":"+27821112222","lat":-26.195,"lng":28.03},
        {"id":"d2","name":"Johan B","phone":"+27823334444","lat":-26.107,"lng":28.05},
        {"id":"d3","name":"Ayesha P","phone":"+27824445555","lat":-29.858,"lng":31.02},
    ]
    DB["addresses"] = [
        {"id":"a1","customer_id":"u1","label":"Home","address":"Vilakazi St, Soweto, Johannesburg","lat":-26.2389,"lng":27.9086},
        {"id":"a2","customer_id":"u1","label":"Work","address":"Sandton Dr, Sandton, Johannesburg","lat":-26.1076,"lng":28.0570},
        {"id":"a3","customer_id":"u2","label":"Home","address":"Burnett St, Hatfield, Pretoria","lat":-25.7470,"lng":28.2380},
        {"id":"a4","customer_id":"u3","label":"Home","address":"Breakwater Blvd, Cape Town","lat":-33.9036,"lng":18.4220},
        {"id":"a5","customer_id":"u2","label":"Work","address":"Lighthouse Rd, Umhlanga, Durban","lat":-29.7267,"lng":31.0864},
    ]
    DB["promotions"] = [
        {"code":"PAYDAY20","percent":20,"desc":"20% off payday"},
        {"code":"STUDENT10","percent":10,"desc":"10% student"},
    ]
    DB["reviews"] = [
        {"id":"rev1","restaurant_id":"r1","customer_id":"u1","stars":5,"text":"Best bunny in Durban!"},
        {"id":"rev2","restaurant_id":"r2","customer_id":"u2","stars":4,"text":"Burger was fire"},
    ]
    DB["orders"] = []