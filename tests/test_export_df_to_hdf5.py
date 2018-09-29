import pytest
import pandas as pd
import holoviews as hv
from .context import scripts
from scripts import export_db_to_hdf5 as exp_hdf5


def test_db_has_correct_name():
    assert exp_hdf5.DB_FILENAME == 'flight.db'

def test_db_table_has_correct_name():
    assert exp_hdf5.TABLE_NAME == 'flights'

# @pytest.mark.skip('TODO')
def test_transform_coords_raises_KeyError_when_latitude_is_missing():
    df = pd.DataFrame({'some_column': ['value0', 'value1']})
    with pytest.raises(KeyError):
        exp_hdf5.transform_coords(df)

def test_transform_coords_does_not_mutate_input_dataframe():
    df_in = pd.DataFrame({'latitude': [51.509865], 'longitude': [-0.118092]})
    df = exp_hdf5.transform_coords(df_in)
    assert  df.latitude.iloc[0] != df_in.latitude.iloc[0]
    assert  df.longitude.iloc[0] != df_in.longitude.iloc[0]

def test_transform_coords_does_not_alter_lat_long_length():
    df_in = pd.DataFrame({'latitude': [51.509865], 'longitude': [-0.118092]})
    df = exp_hdf5.transform_coords(df_in)
    assert len(df.latitude) == len(df_in.latitude)
    assert len(df.longitude) == len(df_in.longitude)

def test_split_flights_raises_AttributeError():
    """This occurs when the input dataframe lacks the time_position column."""
    df_in = pd.DataFrame({'latitude': [51.509865], 'longitude': [-0.118092]})
    df = exp_hdf5.transform_coords(df_in)
    dataset = hv.Dataset(df)
    with pytest.raises(AttributeError):
        exp_hdf5.split_flights(dataset)
    
def test_split_flights_raises_ValueError():
    d = {
        'latitude': [51.509865],
        'longitude': [-0.118092],
        'time_position': [1538239469.0],
    }
    df_in = pd.DataFrame(d)
    df = exp_hdf5.transform_coords(df_in)
    dataset = hv.Dataset(df)
    with pytest.raises(ValueError):
        exp_hdf5.split_flights(dataset)
    