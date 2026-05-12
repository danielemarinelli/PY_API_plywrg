import pytest
from faker import Faker
from playwright.sync_api import Playwright
from datetime import datetime, timedelta

# -------------------------------------------------------------------
# Test: Create Booking (POST request with static body)
# Request Type: POST
# Data : Dynamic data using Faker library
# SWAGGER ONLINE ===> https://restful-booker.herokuapp.com/apidoc/index.html#api-Booking-CreateBooking
# -------------------------------------------------------------------

@pytest.mark.sanity
@pytest.mark.post
def test_create_booking(playwright:Playwright):
    base_url = "https://restful-booker.herokuapp.com"

    request_context = playwright.request.new_context(
        ignore_https_errors=True   # 🔧 This fixes the SSL issue --> unable to get local issuer certificate
    )

    # Generate dynamic request body using Faker library
    fake = Faker()

    first_name=fake.first_name()
    last_name=fake.last_name()
    total_price=fake.random_int(min=100, max=5000)
    deposit_paid=fake.boolean()
    checkin_date = datetime.now().strftime("%Y-%m-%d") # current date in format accepted by JSON body (date not generated with Faker library)
    checkout_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")  # current date + shift 5 days for a gap
    additional_needs=fake.word()


    request_body = {
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": total_price,
        "depositpaid": deposit_paid,
        "bookingdates": {
            "checkin": checkin_date,
            "checkout": checkout_date
        },
        "additionalneeds": additional_needs
    }

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
    assert booking["firstname"] == first_name
    assert booking["lastname"] == last_name
    assert booking["totalprice"] == total_price
    assert booking["depositpaid"] is deposit_paid
    assert booking["additionalneeds"] == additional_needs

    # Validate booking dates (nested JSON object)
    assert booking["bookingdates"]["checkin"] == checkin_date
    assert booking["bookingdates"]["checkout"] == checkout_date

    # Close the API context
    request_context.dispose()
