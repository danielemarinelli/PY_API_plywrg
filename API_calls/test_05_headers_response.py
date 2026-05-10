from playwright.sync_api import Playwright


def test_headers_in_response(playwright:Playwright):
    request_context=playwright.request.new_context(
        ignore_https_errors=True  # 🔧 This fixes the SSL issue --> unable to get local issuer certificate
    )

    response=request_context.get("https://www.google.com/")

    assert response.status_text=="OK"   #assert response.ok
    assert response.status==200

    # Extract all the headers in <k,v> so dictionary form
    headers=response.headers

    for key,value in headers.items():  #items() returns key and value
        #print(key,value)
        print(f"{key}===>{value}")

    # validate specific headers values (many headers change values, so validate only the constant ones)
    print("The value of Content-Type======>",headers.get("content-type"))
    assert "text/html" in headers.get("content-type") # get() returns the value of key=content-type [partial value with 'in' operator]
    assert "gzip" ==headers.get("content-encoding")  #get() returns the value of key=content-encoding [exact value with '==' operator]

    #validate specific header presence (always lower cases)
    assert "server" in headers
    assert "set-cookie" in headers

