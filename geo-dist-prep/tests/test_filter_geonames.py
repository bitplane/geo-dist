import io

import pytest
from geo_dist_prep.filter_geonames import process_tsv


@pytest.fixture
def columns():
    return ["osm_type", "class", "type", "osm_id", "lon", "lat", "name", "geohash"]


@pytest.fixture
def columns_str(columns):
    return "\t".join(columns)


@pytest.fixture
def filters():
    return {
        "osm_type": "node",
        "class": "place",
        "type": "city|village|hamlet|borough|suburb|quarter|neighbourhood",
    }


def test_has_header():
    data = "\t".join(["osm_type", "class", "type", "osm_id", "lon", "lat", "name"])
    infile = io.StringIO(data)

    generator_output = list(process_tsv(columns, filters, infile))

    assert generator_output[0] == columns, "Header not correctly yielded"


def test_row_filtered(columns, columns_str, filters):
    data = "\t".join(
        ["not_a_node", "place", "city", "12345", "12.34", "56.78", "TestCity2"]
    )
    infile = io.StringIO(f"{columns_str}\n{data}\n")

    generator_output = list(process_tsv(columns, filters, infile))

    assert len(generator_output) == 1, "Filtered row should not appear"


def test_row_not_filtered(columns, columns_str, filters):
    data = "\t".join(["node", "place", "city", "12345", "12.34", "56.78", "TestCity"])
    infile = io.StringIO(f"{columns_str}\n{data}\n")

    generator_output = list(process_tsv(columns, filters, infile))

    assert len(generator_output) == 2, "Unfiltered row should appear"


def test_geohash_calculation(columns, columns_str, filters):
    data = "\t".join(["node", "place", "city", "12345", "12.34", "56.78", "TestCity"])
    infile = io.StringIO(f"{columns_str}\n{data}\n")

    generator_output = list(process_tsv(columns, filters, infile))
    geohash_value = generator_output[1][-1]

    assert geohash_value == "u60g0b3xqz4v", "Wrong geohash value"


def test_missing_lat_lon(columns, columns_str, filters):
    data = "\t".join(["node", "place", "city", "12345", "", "", "TestCity"])
    infile = io.StringIO(f"{columns_str}\n{data}\n")

    generator_output = list(process_tsv(columns, filters, infile))
    geohash_value = generator_output[1][-1]

    assert geohash_value == "", "Geohash value should be empty for missing lat/lon"


def test_exception_in_row_processing(columns, columns_str, filters):
    invalid = "not a number"
    data = "\t".join(["node", "place", "city", "12345", "12.34", invalid, "TestCity"])
    infile = io.StringIO(f"{columns_str}\n{data}\n")

    generator_output = list(process_tsv(columns, filters, infile))

    assert len(generator_output) == 1, "Row causing exception should not appear"
