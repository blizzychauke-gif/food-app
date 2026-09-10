import requests
from app.providers.maps.interface import MapsProvider, Coords, Place, RouteInfo
class GoogleMapsProvider(MapsProvider):
    BASE='https://maps.googleapis.com/maps/api'
    def __init__(self,key=None): self.key=key
    def _get(self,path,params):
        if not self.key: raise RuntimeError('GOOGLE_MAPS_API_KEY is not configured')
        r=requests.get(f'{self.BASE}/{path}',params={**params,'key':self.key},timeout=15); r.raise_for_status(); data=r.json()
        if data.get('status') not in ('OK','ZERO_RESULTS'): raise RuntimeError(data.get('error_message') or data.get('status'))
        return data
    def autocomplete(self,query):
        d=self._get('place/autocomplete/json',{'input':query,'components':'country:za'})
        return [Place(x['description'],x['description'],0,0) for x in d.get('predictions',[])[:5]]
    def geocode(self,address):
        d=self._get('geocode/json',{'address':address}); res=d.get('results',[])
        if not res:return None
        loc=res[0]['geometry']['location']; return Coords(loc['lat'],loc['lng'])
    def reverse_geocode(self,lat,lng):
        d=self._get('geocode/json',{'latlng':f'{lat},{lng}'}); return d.get('results',[{'formatted_address':f'{lat},{lng}'}])[0]['formatted_address']
    def route(self,origin,dest):
        d=self._get('directions/json',{'origin':f'{origin.lat},{origin.lng}','destination':f'{dest.lat},{dest.lng}','mode':'driving'})
        leg=d['routes'][0]['legs'][0]; poly=[]
        # Decode Google encoded polyline without extra dependency.
        s=d['routes'][0]['overview_polyline']['points']; i=0; lat=lng=0
        while i<len(s):
            for coord in ('lat','lng'):
                shift=result=0
                while True:
                    b=ord(s[i])-63;i+=1;result|=(b&31)<<shift;shift+=5
                    if b<32:break
                delta=~(result>>1) if result&1 else result>>1
                if coord=='lat':lat+=delta
                else:lng+=delta
            poly.append({'lat':lat/1e5,'lng':lng/1e5})
        return RouteInfo(distance_km=round(leg['distance']['value']/1000,2),eta_min=max(1,round(leg['duration']['value']/60)),polyline=poly)
