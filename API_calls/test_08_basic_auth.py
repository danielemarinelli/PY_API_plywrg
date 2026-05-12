import base64

import pytest
from playwright.sync_api import Playwright

# 1) Basic Authentication 1
# url: https://httpbin.org/basic-auth/user/pass
# username: user
# password : pass

@pytest.mark.auth
def test_basic_auth_resp_body_json(playwright: Playwright):
     request_context = playwright.request.new_context()
#     process to send user and password in basic Auth
#     convert from string format to encode format with base64 library and the decode it
     credentials = base64.b64encode(b"user:pass").decode("utf-8")
#     user and password will be passed with headers and key ==> 'Authorization'
     response = request_context.get("https://httpbin.org/basic-auth/user/pass",
                                    headers={"Authorization": f"Basic {credentials}"}
                                    )
     assert response.status == 200
     response_body = response.json()
     print("Response body:", response_body)

     request_context.dispose()


# 2) Basic Authentication 2
# url: http://the-internet.herokuapp.com/basic_auth
# username: admin
# password : admin
@pytest.mark.auth
def test_basic_auth_resp_body_text(playwright: Playwright):
     request_context = playwright.request.new_context()

     credentials = base64.b64encode(b"admin:admin").decode("utf-8")

     response = request_context.get("http://the-internet.herokuapp.com/basic_auth",
                                    headers={"Authorization": f"Basic {credentials}"}
                                    )
     assert response.status == 200
     response_body = response.text()   # the response is in TEXT format, not in JSON format, so we use text() method
     print("Response body:", response_body)

     request_context.dispose()