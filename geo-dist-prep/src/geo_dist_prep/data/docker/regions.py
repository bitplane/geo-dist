from dataclasses import dataclass

import psutil

SYSTEM_RAM = psutil.virtual_memory().total / (1024**3)


@dataclass(frozen=True)
class Region:
    name: str
    file: str
    codes: frozenset[str]
    ram: int

    @property
    def too_large(self):
        return self.ram + 1 > SYSTEM_RAM


REGIONS = [
    Region(
        name="britain_and_ireland",
        file="https://download.geofabrik.de/europe/britain-and-ireland-latest.osm.pbf",
        codes=frozenset(code for code in ("gb|ie|im|gg|je").split("|")),
        ram=6,  # 1.84gb peak RAM
    ),
    Region(
        name="africa",
        file="https://download.geofabrik.de/africa-latest.osm.pbf",
        codes=frozenset(
            code
            for code in (
                "sh|ta|dz|ao|bj|bw|bf|bi|cv|cm|cf|td|km|cg|cd|dj|eg|gq|er|sz|et|"
                "ga|gm|gh|gn|gw|ci|ke|ls|lr|ly|mg|mw|ml|mr|mu|ma|mz|na|ne|ng|re|"
                "rw|st|sn|sc|sl|so|za|ss|sd|tz|tg|tn|ug|eh|zm|zw"
            ).split("|")
        ),
        ram=12,  # ?? peak RAM (5.01gb)
    ),
    Region(
        name="antarctica",
        file="https://download.geofabrik.de/antarctica-latest.osm.pbf",
        codes=frozenset(("tf", "gs", "aq")),
        ram=2,  # 0.46gb peak RAM
    ),
    Region(
        name="asia",
        file="https://download.geofabrik.de/asia-latest.osm.pbf",
        codes=frozenset(
            code
            for code in (
                "ps|io|tw|af|ae|am|az|bh|bd|bt|bn|kh|cn|cy|ge|in|id|ir|iq|il|jp|"
                "jo|kz|kw|kg|la|lb|lk|my|mv|mn|mm|np|kp|om|pf|pk|ph|qa|ru|sa|sg|"
                "kr|lk|sy|tj|th|tl|tm|tr|ae|uz|vn|ye"
            ).split("|")
        ),
        ram=24,  # 18.5gb peak RAM (??) (13gb file)
    ),
    Region(
        name="australia_oceania",
        file="https://download.geofabrik.de/australia-oceania-latest.osm.pbf",
        codes=frozenset(
            code
            for code in (
                "as|au|ck|fj|pf|gu|ki|mh|fm|nr|nc|nz|nu|nf|mp|pw|pg|pn|ws|sb|tk|"
                "to|tv|vu|wf|um"
            ).split("|")
        ),
        ram=4,  # 1.22gb peak RAM
    ),
    Region(
        name="europe",
        file="https://download.geofabrik.de/europe-latest.osm.pbf",
        codes=frozenset(
            code
            for code in (
                "im|je|fo|gg|gi|al|ad|am|at|by|be|ba|bg|hr|cy|cz|dk|ee|fi|fr|ge|"
                "de|gr|hu|is|ie|it|xk|lv|li|lt|lu|mk|mt|md|mc|me|nl|no|pl|pt|ro|"
                "sm|rs|sk|si|es|se|ch|ua|gb|va"
            ).split("|")
        ),
        ram=72,  # ???? too big! file is 28g, crashes on 60gb
    ),
    Region(
        name="central_america",
        file="https://download.geofabrik.de/central-america-latest.osm.pbf",
        codes=frozenset(code for code in ("bz|cr|sv|gt|hn|ni|pa").split("|")),
        ram=4,  # 1.12gb peak RAM (580mb)
    ),
    Region(
        name="north_america",
        file="https://download.geofabrik.de/north-america-latest.osm.pbf",
        codes=frozenset(
            code
            for code in (
                "bq|gl|ai|ag|bs|bb|bm|vg|ca|ky|dm|do|gd|gp|ht|jm|mq|mx|ms|an|"
                "cu|pr|kn|lc|pm|vc|tt|tc|us|vi"
            ).split("|")
        ),
        ram=28,  # guess about 20gb to 22gb?
    ),
    Region(
        name="south_america",
        file="https://download.geofabrik.de/south-america-latest.osm.pbf",
        codes=frozenset(
            code for code in "ar|bo|br|cl|co|ec|fk|gy|py|pe|sr|uy|ve".split("|")
        ),
        ram=10,  # 5.65gb peak RAM (3.87gb)
    ),
]


def get_region_for_country(country_code):
    for region in REGIONS:
        if country_code in region.codes:
            return region
    raise ValueError(f"No container found for {country_code}")


def group_countries_by_region(country_codes):
    ret = {}
    for code in country_codes:
        region = get_region_for_country(code)
        ret[region] = ret.get(region, []) + [code]
    return ret
