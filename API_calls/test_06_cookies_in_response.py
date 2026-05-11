from playwright.sync_api import Playwright


def test_cookies_in_response(playwright:Playwright):
    request_context=playwright.request.new_context(
        ignore_https_errors=True  # 🔧 This fixes the SSL issue --> unable to get local issuer certificate
    )

    response=request_context.get("https://www.google.com/")

    assert response.status_text=="OK"   #assert response.ok
    assert response.status==200

    # Extract all the cookies from the request context, not from the response (like with the headers)
    cookies=request_context.storage_state()["cookies"]

    for c in cookies: #usually the name does not change, but value, domain change
        print(f"{c['name']}==>{c['value']}==>{c['domain']}")

    # Cookies values are not constant
    # Check if 'AEC' cookie exists
    aec_cookie= None

    for c in cookies:   # Verify the existing of cookies and we can't get them from the response, but from the request_context.storage_state()
        if c["name"] =="AEC":
            aec_cookie=c # the cookie "AEC" is present in the list
            break

    # adding assertion with additional description, if assert fails print the message 'Cookie AEC not found'
    assert aec_cookie is not None, "Cookie 'AEC' not found"

    # Printing details of 'AEC' Cookie

    print(aec_cookie['name'])
    print(aec_cookie['value'])
    print(aec_cookie['domain'])
    print(aec_cookie['path'])
    print(aec_cookie['expires'])




