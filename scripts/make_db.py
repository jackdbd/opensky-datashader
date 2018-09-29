"""Store the data in a SQLite database.
Usage:
    $ python make_db.py
    $ python make_db.py -v
"""
import os
import time
import json
import sqlite3
import requests
import pandas as pd
import sqlalchemy as sa
import argparse

# TODO: make this script a cron job and run it on Amazon Lambda


HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(HERE, '..', 'data'))
DB_FILENAME = 'flight.db'
DB_FILEPATH = os.path.abspath(os.path.join(DATA_DIR, DB_FILENAME))
TABLE_NAME = 'flights'
API_URL = 'https://opensky-network.org/api/states/all'


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="If set, increase output verbosity"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    t0 = time.time()
    engine = sa.create_engine(f'sqlite:///{DB_FILEPATH}')

    cols = [
        'icao24', 'callsign', 'origin', 'time_position', 'time_velocity',
        'longitude', 'latitude', 'altitude', 'on_ground', 'velocity', 'heading',
        'vertical_rate', 'sensors', 'bo0', 'bo1', 'bo2', 'bo2'
        ]

    req = requests.get(API_URL)
    content = json.loads(req.content)
    states = content['states']
    df = pd.DataFrame(states, columns=cols)
    df['timestamp'] = content['time']
    df.to_sql(TABLE_NAME, con=engine, index=False, if_exists='append')
    t1 = time.time()
    print(f'Done in {(t1 - t0):.2f} seconds')


if __name__ == '__main__':
    main()
