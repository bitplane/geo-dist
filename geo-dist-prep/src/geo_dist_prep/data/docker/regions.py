from dataclasses import dataclass


@dataclass
class Region:
    name: str
    file: str
    codes: set[str]


REGIONS = [
    Region(
        name="africa",
        file="https://download.geofabrik.de/africa-latest.osm.pbf",
        codes={
            code
            for code in (
                "sh|ta|dz|ao|bj|bw|bf|bi|cv|cm|cf|td|km|cg|cd|dj|eg|gq|er|sz|et|"
                "ga|gm|gh|gn|gw|ci|ke|ls|lr|ly|mg|mw|ml|mr|mu|ma|mz|na|ne|ng|re|"
                "rw|st|sn|sc|sl|so|za|ss|sd|tz|tg|tn|ug|eh|zm|zw"
            ).split("|")
        },
    ),
    Region(
        name="antarctica",
        file="https://download.geofabrik.de/antarctica-latest.osm.pbf",
        codes={"tf", "gs", "aq"},
    ),
    Region(
        name="asia",
        file="https://download.geofabrik.de/asia-latest.osm.pbf",
        codes={
            code
            for code in (
                "ps|io|tw|af|ae|am|az|bh|bd|bt|bn|kh|cn|cy|ge|in|id|ir|iq|il|jp|"
                "jo|kz|kw|kg|la|lb|lk|my|mv|mn|mm|np|kp|om|pf|pk|ph|qa|ru|sa|sg|"
                "kr|lk|sy|tj|th|tl|tm|tr|ae|uz|vn|ye"
            ).split("|")
        },
    ),
    Region(
        name="australia_oceania",
        file="https://download.geofabrik.de/australia-oceania-latest.osm.pbf",
        codes={
            code
            for code in (
                "as|au|ck|fj|pf|gu|ki|mh|fm|nr|nc|nz|nu|nf|mp|pw|pg|pn|ws|sb|tk|"
                "to|tv|vu|wf|um"
            ).split("|")
        },
    ),
    Region(
        name="europe",
        file="https://download.geofabrik.de/europe-latest.osm.pbf",
        codes={
            code
            for code in (
                "im|je|fo|gg|gi|al|ad|am|at|by|be|ba|bg|hr|cy|cz|dk|ee|fi|fr|ge|"
                "de|gr|hu|is|ie|it|xk|lv|li|lt|lu|mk|mt|md|mc|me|nl|no|pl|pt|ro|"
                "sm|rs|sk|si|es|se|ch|ua|gb|va"
            ).split("|")
        },
    ),
    Region(
        name="central_america",
        file="https://download.geofabrik.de/central-america-latest.osm.pbf",
        codes={code for code in ("bz|cr|sv|gt|hn|ni|pa").split("|")},
    ),
    Region(
        name="north_america",
        file="https://download.geofabrik.de/north-america-latest.osm.pbf",
        codes={
            code
            for code in (
                "bq|gl|ai|ag|bs|bb|bm|vg|ca|ky|dm|do|gd|gp|ht|jm|mq|mx|ms|an|"
                "cu|pr|kn|lc|pm|vc|tt|tc|us|vi"
            ).split("|")
        },
    ),
    Region(
        name="south_america",
        file="https://download.geofabrik.de/south-america-latest.osm.pbf",
        codes={code for code in ("ar|bo|br|cl|co|ec|fk|gy|py|pe|sr|uy|ve").split("|")},
    ),
]
