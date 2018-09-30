import os
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


def split_flights(dataset):
    # TODO: something here fails
    df = dataset.data.copy().reset_index(drop=True)
    df = df[np.logical_not(df.time_position.isnull())]
    empty = df[:1].copy()
    empty.loc[0, :] = (np.NaN,) * 14
    paths = []
    for gid, group in df.groupby("icao24"):
        times = group.time_position
        for split_df in np.split(
            group.reset_index(drop=True), np.where(times.diff() > 600)[0]
        ):
            if len(split_df) > 20:
                paths += [split_df, empty]
    split = pd.concat(paths, ignore_index=True)
    split["ascending"] = split.vertical_rate > 0
    return split


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="If set, increase output verbosity"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    t0 = time.time()
    engine = sa.create_engine(f"sqlite:///{DB_FILEPATH}")
    sql = """
    SELECT * from flights;
    """
    df = transform_coords(pd.read_sql(sql, engine))
    dataset = hv.Dataset(df)
    flightpaths = split_flights(dataset)
    # Remove unused columns
    # flightpaths = flightpaths[['longitude', 'latitude', 'origin', 'on_ground', 'ascending','velocity']]
    # flightpaths['origin'] = flightpaths.origin.astype(str)

    # flightpaths.to_hdf(HDF5_PATH, 'flights')

    t1 = time.time()
    print(f"Done in {(t1 - t0):.2f} seconds")


if __name__ == "__main__":
    main()
