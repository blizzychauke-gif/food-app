import math
from app.providers.maps.interface import MapsProvider, Coords, Place, RouteInfo
SA_PLACES=[
    Place("Sandton City","Sandton Dr, Sandton, Johannesburg",-26.1076,28.0570),
    Place("Vilakazi St","Vilakazi St, Soweto, Johannesburg",-26.2389,27.9086),
    Place("V&A Waterfront","Breakwater Blvd, Cape Town",-33.9036,18.4220),
    Place("Umhlanga Rocks","Lighthouse Rd, Umhlanga, Durban",-29.7267,31.0864),
    Place("Hatfield Plaza","Burnett St, Hatfield, Pretoria",-25.7470,28.2380),
    Place("Florida Road","Florida Rd, Durban",-29.8587,31.0218),
    Place("Long Street","Long St, Cape Town",-33.9249,18.4241),
    Place("Braamfontein","Jorissen St, Braamfontein, JHB",-26.1929,28.0340),
]
def hav(a:Coords,b:Coords):
    R=6371; import math as m
    dlat=m.radians(b.lat-a.lat); dlng=m.radians(b.lng-a.lng)
    h=m.sin(dlat/2)**2+m.cos(m.radians(a.lat))*m.cos(m.radians(b.lat))*m.sin(dlng/2)**2
    return 2*R*m.asin(m.sqrt(h))
class MockMapsProvider(MapsProvider):
    def autocomplete(self, query: str):
        q=query.lower(); return [p for p in SA_PLACES if q in p.name.lower() or q in p.address.lower()][:5]
    def geocode(self, address: str):
        r=self.autocomplete(address); return Coords(r[0].lat,r[0].lng) if r else None
    def reverse_geocode(self, lat, lng): return f"Mock address near {lat:.4f},{lng:.4f}, South Africa"
    def route(self, origin, dest):
        d=hav(origin,dest); eta=int(d/30*60)+5
        pts=[{"lat":origin.lat+(dest.lat-origin.lat)*i/20,"lng":origin.lng+(dest.lng-origin.lng)*i/20} for i in range(21)]
        return RouteInfo(distance_km=round(d,2), eta_min=eta, polyline=pts)