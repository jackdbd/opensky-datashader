import pytest
import json
import requests
import lxml.html
from .context import scripts
from scripts import make_db


@pytest.fixture(scope="module")
def api_html():
    res = requests.get(make_db.REST_API_SCHEMA_PAGE)
    yield lxml.html.fromstring(res.content)


@pytest.fixture(scope="module")
def content_json():
    req = requests.get(make_db.API_URL)
    return json.loads(req.content)


def test_rest_api_schema_page_has_expected_number_of_fields(api_html):
    # this is a valid XPath selector in Chrome, but it doesn't work here.
    # fields = api_html.xpath('//div[@id="all-state-vectors"]/div[@id="response"]/div[position()=2]/table/tbody/tr')
    # this is also a valid XPath selector in Chrome, but it doesn't work here.
    # fields = api_html.xpath('//div[@id="all-state-vectors"]/div[@id="response"]/div[2]/table/tbody/tr')
    # this is also a valid XPath selector in Chrome, but it doesn't work here.
    # fields = api_html.xpath('//div[@id="all-state-vectors"]/div[@id="response"]/div[position()=last()]/table/tbody/tr')
    # this is the only one that works both in Chrome and here.
    fields = api_html.xpath(
        '//div[@id="all-state-vectors"]//table/thead/tr/th[contains(text(), "Index")]/parent::*/parent::*/parent::*/tbody/tr'
    )
    assert len(fields) == 17


def test_rest_api_schema_page_has_expected_fields(api_html):
    fields = api_html.xpath(
        '//div[@id="all-state-vectors"]//table/thead/tr/th[contains(text(), "Index")]/parent::*/parent::*/parent::*/tbody/tr/td/em/text()'
    )
    f = make_db.REST_API_SCHEMA_FIELDS
    assert fields[0] == f[0]
    assert fields[1] == f[1]
    assert fields[2] == f[2]
    assert fields[3] == f[3]
    assert fields[4] == f[4]
    assert fields[5] == f[5]
    assert fields[6] == f[6]
    assert fields[7] == f[7]
    assert fields[8] == f[8]
    assert fields[9] == f[9]
    assert fields[10] == f[10]
    assert fields[11] == f[11]
    assert fields[12] == f[12]
    assert fields[13] == f[13]
    assert fields[14] == f[14]
    assert fields[15] == f[15]
    assert fields[16] == f[16]


def test_df_has_timestamp_column(content_json):
    df = make_db.make_df(content_json)
    assert "timestamp" in df.columns


def test_df_has_expected_number_of_columns(content_json):
    df = make_db.make_df(content_json)
    assert len(df.columns) == 18


def test_make_db_has_flag_for_verbosity():
    namespace = make_db.parse_args([])
    assert namespace.verbose == False
    namespace = make_db.parse_args(["-v"])
    assert namespace.verbose == True


def test_make_db_with_unsupported_flags_exits_with_SystemExit_code_2():
    with pytest.raises(SystemExit) as e:
        make_db.parse_args(["-d"])
    assert e.type == SystemExit
    assert e.value.code == 2
