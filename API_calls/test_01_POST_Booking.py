from playwright.sync_api import Playwright


# -------------------------------------------------------------------
# Test: Create Booking (POST request with static body)
# Request Type: POST
# Data : Hardcoded data inside the test  (Not Recommended)
# SWAGGER ONLINE ===> https://restful-booker.herokuapp.com/apidoc/index.html#api-Booking-CreateBooking
# -------------------------------------------------------------------

def test_create_booking(playwright: Playwright):
    base_url = "https://restful-booker.herokuapp.com"

    # step1: with fixture playwright use request context
    # request_context = playwright.request.new_context()

    # Step 1: Create request context with SSL verification disabled
    request_context = playwright.request.new_context(
        ignore_https_errors=True  # 🔧 This fixes the SSL issue --> unable to get local issuer certificate
    )

    # Request body needed before sending the http post (BODY HARDCODED)
    request_body = {
        "firstname": "LeBron",
        "lastname": "James",
        "totalprice": 1043,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-11-01",
            "checkout": "2026-12-24"
        },
        "additionalneeds": "LA Lakers"
    }

    # Send POST request with payload as body
    response = request_context.post(f"{base_url}/booking", data=request_body)

    # Extract response body
    response_body = response.json()
    print(response_body)

    '''
    EXAMPLE OF HOW A RESPONSE BODY IS:
    {
    "bookingid": 5244,
    "booking": {
        "firstname": "LeBron",
        "lastname": "James",
        "totalprice": 1043,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-11-01",
            "checkout": "2026-12-24"
        },
        "additionalneeds": "LA Lakers"
    }
    '''

    # ------------------------------
    # Validations
    # ------------------------------
    assert response.ok
    assert response.status == 200

    # Validate top-level keys of the response
    assert "bookingid" in response_body
    assert "booking" in response_body

    booking = response_body["booking"]

    # Validate booking details
    assert booking["firstname"] == "LeBron"
    assert booking["lastname"] == "James"
    assert booking["totalprice"] == 1043
    assert booking["depositpaid"] is True
    assert booking["additionalneeds"] == "LA Lakers"

    # Validate booking dates (nested JSON object)
    assert booking["bookingdates"]["checkin"] == "2025-11-01"
    assert booking["bookingdates"]["checkout"] == "2026-12-24"

    # Close the API context
    request_context.dispose()
