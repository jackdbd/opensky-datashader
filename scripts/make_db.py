"""Store the data in a SQLite database.

Usage:
    $ python make_db.py
    $ python make_db.py -v
"""
import os
import sys
import time
import json
import requests
import pandas as pd
import sqlalchemy as sa
import argparse

# TODO: make this script a cron job and run it on Amazon Lambda
# TODO: remove SQLAlchemy


HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(HERE, "..", "data"))
DB_FILENAME = "flight.db"
DB_FILEPATH = os.path.abspath(os.path.join(DATA_DIR, DB_FILENAME))
TABLE_NAME = "flights"
API_URL = "https://opensky-network.org/api/states/all"
REST_API_SCHEMA_PAGE = "https://opensky-network.org/apidoc/rest.html"
REST_API_SCHEMA_FIELDS = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
]


def parse_args(args):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="If set, increase output verbosity"
    )
    return parser.parse_args(args)


def make_df(content):
    df = pd.DataFrame(content["states"], columns=REST_API_SCHEMA_FIELDS)
    df["timestamp"] = content["time"]
    return df


def main():  # pragma: no cover
    parse_args(sys.argv[1:])
    t0 = time.time()
    engine = sa.create_engine(f"sqlite:///{DB_FILEPATH}")
    req = requests.get(API_URL)
    content = json.loads(req.content)
    df = make_df(content)
    df.to_sql(TABLE_NAME, con=engine, index=False, if_exists="append")
    t1 = time.time()
    print(f"Done in {(t1 - t0):.2f} seconds")


if __name__ == "__main__":
    main()
