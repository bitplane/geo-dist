from pydantic import BaseModel, Field


class GeoNames(BaseModel):
    name: str
    alternative_names: str
    osm_type: str
    osm_id: int
    class_: str = Field(alias="class")
    type: str
    lon: float
    lat: float
    place_rank: int
    importance: float
    street: str
    city: str
    county: str
    state: str
    country: str
    country_code: str
    display_name: str
    west: float
    south: float
    east: float
    north: float
    wikidata: str
    wikipedia: str
    housenumbers: str
