import base64
import secrets
import string
import hashlib
import re
from auth.util import search_code_path

from nose.tools import *


def test():
    encoded_code_verifier = secrets.token_urlsafe(32).encode(encoding='ASCII')
    hashed_code_challenge_bytes = hashlib.sha256(encoded_code_verifier).digest()
    print(base64.urlsafe_b64encode(hashed_code_challenge_bytes).decode('ascii'))


# GET /?code=753ae17a-149c-42a4-9754-958aa23b5c36&state=jMDNgB4skpKhdd9k69hSfZI0GhZHWQ5Rf60CLTor2lE
def test_search_code_path():
    # given
    code = "753ae17a-149c-42a4-9754-958aa23b5c36"
    state = "jMDNgB4skpKhdd9k69hSfZI0GhZHWQ5Rf60CLTor2lE"
    path = "/?code={}&state={}".format(code, state)

    # assert
    assert_equal(code, search_code_path(path, "code"))
    assert_equal(state, search_code_path(path, "state"))

# {}?response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri={}&client_id={}&state={}&code_challenge={}&code_challenge_method=S256
