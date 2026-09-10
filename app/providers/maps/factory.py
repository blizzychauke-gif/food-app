from app.config import settings
from app.providers.maps.mock import MockMapsProvider
from app.providers.maps.google_maps import GoogleMapsProvider
import os
def get_maps_provider():
    if settings.MAP_PROVIDER=="google": return GoogleMapsProvider(os.getenv("GOOGLE_MAPS_API_KEY"))
    return MockMapsProvider()