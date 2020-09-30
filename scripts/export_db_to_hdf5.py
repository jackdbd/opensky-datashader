import os
import sys
import time
import argparse
import numpy as np
import pandas as pd
import sqlalchemy as sa
import holoviews as hv
from cartopy import crs


HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(HERE, "..", "data"))
DB_FILENAME = "flight.db"
DB_FILEPATH = os.path.abspath(os.path.join(DATA_DIR, DB_FILENAME))
TABLE_NAME = "flights"
HDF5_PATH = os.path.abspath(os.path.join(DATA_DIR, "opensky.h5"))


def transform_coords(df):
    df = df.copy()
    lons = np.array(df["longitude"])
    lats = np.array(df["latitude"])
    coords = crs.GOOGLE_MERCATOR.transform_points(crs.PlateCarree(), lons, lats)
    df["longitude"] = coords[:, 0]
    df["latitude"] = coords[:, 1]
    return df


def find_a_name_for_this_function(conn):
    sql = """
    SELECT
      f.icao24,
      MIN(f.time_position) AS ts_min,
      MAX(f.time_position) AS ts_max,
      f.longitude,
      f.latitude,
      f.geo_altitude,
      f.baro_altitude,
      f.velocity,
      COUNT(*) AS num
    FROM flights AS f
    WHERE
      f.time_position IS NOT NULL AND
	  f.on_ground IS 0
    GROUP BY f.icao24
    HAVING
      num > 1 AND
      (ts_max - ts_min) > 0;
    """
    df = transform_coords(pd.read_sql(sql, conn))
    return df


def split_flights(dataset):
    # num_datapoints = 21
    num_datapoints = 1
    df = dataset.data.copy().reset_index(drop=True)
    df = df[~df.time_position.isnull()]
    # df = df[np.logical_not(df.time_position.isnull())]
    empty = df[:1].copy()
    empty.loc[0, :] = (np.NaN,) * df.shape[1]
    paths = []
    for _gid, group in df.groupby("icao24"):
        times = group.time_position
        for split_df in np.split(
            group.reset_index(drop=True), np.where(times.diff() > 600)[0]
        ):
            if len(split_df) >= num_datapoints:
                paths += [split_df, empty]
    split = pd.concat(paths, ignore_index=True)
    split["ascending"] = split.vertical_rate > 0
    return split


def parse_args(args):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="If set, increase output verbosity"
    )
    return parser.parse_args(args)


def main():  # pragma: no cover
    parse_args(sys.argv[1:])
    t0 = time.time()
    engine = sa.create_engine(f"sqlite:///{DB_FILEPATH}")
    sql = """
    SELECT * from flights;
    """
    df = transform_coords(pd.read_sql(sql, engine))
    ddf = find_a_name_for_this_function(engine)
    print(ddf.shape)

    dataset = hv.Dataset(df)
    print("=== dataset ===", dataset)
    flightpaths = split_flights(dataset)
    # Remove unused columns
    flightpaths = flightpaths[['longitude', 'latitude', 'origin_country', 'on_ground', 'ascending','velocity']]
    flightpaths['origin_country'] = flightpaths.origin_country.astype(str)
    flightpaths.to_hdf(HDF5_PATH, 'flights')

    t1 = time.time()
    print(f"Done in {(t1 - t0):.2f} seconds")


if __name__ == "__main__":
    main()
