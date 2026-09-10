from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
@dataclass
class Coords: lat: float; lng: float
@dataclass
class Place: name: str; address: str; lat: float; lng: float
@dataclass
class RouteInfo: distance_km: float; eta_min: int; polyline: list
class MapsProvider(ABC):
    @abstractmethod
    def autocomplete(self, query: str) -> List[Place]: ...
    @abstractmethod
    def geocode(self, address: str) -> Optional[Coords]: ...
    @abstractmethod
    def reverse_geocode(self, lat: float, lng: float) -> str: ...
    @abstractmethod
    def route(self, origin: Coords, dest: Coords) -> RouteInfo: ...