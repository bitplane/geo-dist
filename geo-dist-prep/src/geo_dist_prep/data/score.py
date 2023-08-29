from datetime import datetime

from sqlalchemy import create_engine, delete, text, update
from sqlalchemy.orm import sessionmaker

from ..data import GEONAMES_DB
from ..schemas.geoname import GeoName
from ..schemas.helpers import grid_coord


def score_nodes():
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Session = sessionmaker(bind=engine)
    session = Session()

    # first, set all scores to 0
    print("score: resetting scores")
    session.query(GeoName).update({GeoName.score: 0})

    for grid_size in (1, 2, 4, 8, 16, 32, 64, 128, 256):
        print("score: find important nodes in", grid_size, "km grid")

        grid_column = grid_coord(GeoName, grid_size).label("grid_coord")
        table_plus_grid = session.query(GeoName).add_columns(grid_column)
        by_importance = table_plus_grid.order_by(GeoName.importance)
        distinct = by_importance.group_by("grid_coord").distinct().subquery()

        update_stmt = (
            update(GeoName)
            .values(score=grid_size)
            .where(GeoName.osm_id == distinct.c.osm_id)
        )
        result = session.execute(update_stmt)
        print("score: updated", result.rowcount, "rows")

    print("score: committing changes")
    session.commit()

    delete_stmt = delete(GeoName).where(GeoName.score == 0)
    print("score: deleting records with 0km importance")
    result = session.execute(delete_stmt)
    print("score: deleting", result.rowcount, "rows")
    session.commit()

    print("score: compacting database")
    session.execute(text("VACUUM"))

    print("score: done")


if __name__ == "__main__":
    score_nodes()

    print("score: finished at", datetime.now().isoformat())
