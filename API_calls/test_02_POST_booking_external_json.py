import json
from playwright.sync_api import Playwright
import pytest

# -------------------------------------------------------------------
# Test: Create Booking (POST request with static body from an external file)
# Request Type: POST
# Data : External json file
# SWAGGER ONLINE ===> https://restful-booker.herokuapp.com/apidoc/index.html#api-Booking-CreateBooking
# -------------------------------------------------------------------

@pytest.mark.sanity
@pytest.mark.post
def test_create_booking(playwright:Playwright):
    base_url = "https://restful-booker.herokuapp.com"

    request_context = playwright.request.new_context(
        ignore_https_errors=True  # 🔧 This fixes the SSL issue --> unable to get local issuer certificate
    )

    # Load request body from external JSON file
    file = open("testdata/post_request_body.json", "r")
    request_body = json.load(file)

    # Send POST request
    response = request_context.post(f"{base_url}/booking", data=request_body)

    # Extract response body
    response_body = response.json()
    print(response_body)

    # ------------------------------
    # Validations
    # ------------------------------
    assert response.ok
    assert response.status == 200

    # Validate top-level keys
    assert "bookingid" in response_body
    assert "booking" in response_body

    booking = response_body["booking"]

    # Validate booking details
    assert booking["firstname"] == "Nikola"
    assert booking["lastname"] == "Jokic"
    assert booking["totalprice"] == 1077
    assert booking["depositpaid"] is True
    assert booking["additionalneeds"] == "Denver Nuggets"

    # Validate booking dates (nested JSON object)
    assert booking["bookingdates"]["checkin"] == "2024-07-01"
    assert booking["bookingdates"]["checkout"] == "2025-07-05"

    # Close the API context
    request_context.dispose()
