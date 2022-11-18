import uuid

from nose.tools import *
from auth.auth import parse_auth_code


def test_code_parse():
    # given
    code = uuid.uuid4().__str__()
    assert_equal(code, parse_auth_code(f"/?code={code}"))
