from .context import scripts
from scripts import make_db


def test_answer():
    assert make_db.API_URL == 'https://opensky-network.org/api/states/all'
