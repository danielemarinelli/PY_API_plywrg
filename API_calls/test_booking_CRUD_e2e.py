"""
1) Create Booking (POST) ---> BookingID
2) Get Booking Details (GET) - By ID, By Names, By Dates
3) Create Token (POST /auth)
4) Partial Update Booking (PATCH)  --> need TOKEN
5) Full Update Booking (PUT)       --> need TOKEN
6) Delete Booking (DELETE)         --> need TOKEN
"""

import pytest
import json
from playwright.sync_api import Playwright
from pathlib import Path

# -------------------------------------------------------------------
# Base URL of the RESTful Booker API
# Common for all the API tests
# -------------------------------------------------------------------
base_url = "https://restful-booker.herokuapp.com"


# -------------------------------------------------------------------
# Utility Function: Reads and returns JSON data from a given file path
# This is common for most of tests --> POST, PUT, PATCH , so we can re-use it
# -------------------------------------------------------------------
def read_json(file_path):
    file = open(file_path, "r")
    return json.load(file)


# -------------------------------------------------------------------
# Fixture: Creates a reusable Playwright Request Context for the session
# for all call, we must create a new_context()
# -------------------------------------------------------------------
@pytest.fixture(scope="session")  # with scope='session' , everywhere every time we can return it
def request_context(playwright: Playwright):
    context = playwright.request.new_context(
        ignore_https_errors=True)                # before 'yield' keyword, are all command to be executed before the tests
    yield context                                # this line, if we insert a variable after 'yield' means, the fixture will return the variable (context)
    context.dispose()                            # after 'yield' keyword, are all command to be executed after the tests

global user_home   # Needed to set user home directory

# After the three common things that we need for the testing,
# now we can create write the CRUD tests:

# -------------------------------------------------------------------
# 1) Create Booking (POST)
# -------------------------------------------------------------------
def test_create_booking(request_context):  # passing the context as argument from fixture
    """Create a new booking and validate response"""
    #data_from_json_file = read_json("testdata/post_request_body.json")
    user_home = Path.home()  # Get user home directory
    json_file_path = user_home / "PycharmProjects" / "PythonSelenium" / "_plywrg_API_PY" / "testdata" / "post_request_body.json"
    data_from_json_file = read_json(json_file_path)
    # Send POST request to create booking
    response = request_context.post(f"{base_url}/booking", data=data_from_json_file)

    assert response.ok  # (or)  assert response.status_text=="OK"
    assert response.status == 200

    response_body = response.json()
    print("\nCreate Booking Response:", response_body)

    # Basic validation of response fields
    assert "bookingid" in response_body
    assert "booking" in response_body

    booking_obj = response_body["booking"]

    # Validate key booking details
    assert booking_obj["firstname"] == data_from_json_file["firstname"]
    assert booking_obj["lastname"] == data_from_json_file["lastname"]
    assert booking_obj["totalprice"] == data_from_json_file["totalprice"]
    assert booking_obj["depositpaid"] == data_from_json_file["depositpaid"]
    assert booking_obj["bookingdates"]["checkin"] == data_from_json_file["bookingdates"]["checkin"]
    assert booking_obj["bookingdates"]["checkout"] == data_from_json_file["bookingdates"]["checkout"]

    # Store booking ID and other values globally for reuse in subsequent tests
    global booking_id
    global check_in
    global check_out
    booking_id = response_body["bookingid"]
    check_in = booking_obj["bookingdates"]["checkin"]
    check_out = booking_obj["bookingdates"]["checkout"]


# -------------------------------------------------------------------
# 2) Get Booking Details (GET)
# -------------------------------------------------------------------
def test_get_booking_by_id(request_context):
    """Get booking details using booking ID"""
    # this is an example of url to send with path param => https://restful-booker.herokuapp.com/booking/5244

    get_response = request_context.get(f"{base_url}/booking/{booking_id}")

    assert get_response.ok
    assert get_response.status == 200

    response_body = get_response.json()
    print(f"\nBooking details fetched by ID {booking_id}:", response_body)

    # Validate presence of expected fields
    assert "firstname" in response_body
    assert "lastname" in response_body


def test_get_booking_by_name(request_context):
    """Get bookings filtered by first and last name"""
    # this is an example of url to send with query param => https://restful-booker.herokuapp.com/booking?firstname=Josh&lastname=Allen

    name_params = {"firstname": "Nikola", "lastname": "Jokic"}  # query params in for of a dictionary
    response = request_context.get(f"{base_url}/booking", params=name_params)

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print(f"\nBooking details fetched by Name {name_params}:", response_body)

    # Ensure at least one booking found and contains 'bookingid'
    assert len(response_body) > 0
    for item in response_body:
        assert "bookingid" in item


# this test will run three times (in this case, because three sets of dates in the marker)
@pytest.mark.parametrize("checkin_date, checkout_date", [
    ("2024-07-01", "2025-07-05"),
    ("2024-01-15", "2024-02-20"),
    ("2024-07-01", "2025-07-05"),
])
def test_get_booking_by_dates(request_context,checkin_date, checkout_date):
    """Get bookings filtered by check-in and check-out dates"""
    # this is an example of url to send with query param => https://restful-booker.herokuapp.com/booking?checkin=2014-03-13&checkout=2014-05-21

    date_params = {"checkin": checkin_date, "checkout": checkout_date}  # query params in for of a dictionary
    response = request_context.get(f"{base_url}/booking", params=date_params)

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print(f"\nBooking details fetched by Dates {date_params}:", response_body)

    # Validate that response contains booking IDs
    for item in response_body:
        assert "bookingid" in item



# -------------------------------------------------------------------
# 3) Create Token (POST /auth) --- needed for PUT , PATCH , DELETE calls
# -------------------------------------------------------------------
def test_create_token(request_context):
    """Create an authentication token for further operations"""
    # this is an example of url to send with path param => https://restful-booker.herokuapp.com/auth
    user_home = Path.home()  # Get user home directory

    token_json_file = user_home / "PycharmProjects" / "PythonSelenium" / "_plywrg_API_PY" / "testdata" / "token_request_body.json"
    data_from_token_json_file = read_json(token_json_file)

    token_response = request_context.post(f"{base_url}/auth", data=data_from_token_json_file)

    '''
    The response body of the token generation is:
    HTTP/1.1 200 OK
    {
    "token": "abc123"
    }
    
    '''

    assert token_response.ok
    assert token_response.status == 200

    response_token_body = token_response.json()
    print("\n Token Response:", response_token_body)

    # Basic validation of key response fields
    assert "token" in response_token_body

    global token_generated
    token_generated = response_token_body["token"]



# -------------------------------------------------------------------
# 4) Partial Update Booking (PATCH)  MANDATORY to PASS THE token_generated!!!
# -------------------------------------------------------------------
def test_partial_update_booking(request_context):
    """Partially update an existing booking"""
    # this is an example of url to send with path param =>  https://restful-booker.herokuapp.com/booking/5244

    user_home = Path.home()  # Get user home directory
    json_file_path = user_home / "PycharmProjects" / "PythonSelenium" / "_plywrg_API_PY" / "testdata" / "patch_request_body.json"
    data_from_json_file = read_json(json_file_path)

    patch_response = request_context.patch(f"{base_url}/booking/{booking_id}",
                                           headers={"Cookie": f"token={token_generated}"},  # Cookie is the key and token='value' the value , from swagger we send it as header
                                           data=data_from_json_file)

    assert patch_response.ok
    assert patch_response.status == 200

    response_body = patch_response.json()
    print(f"\nBooking UPDATED details fetched by ID {booking_id}:", response_body)

    # Validate presence of expected fields
    assert "firstname" in response_body
    assert "lastname" in response_body

    # Validate updated fields match request data (passing the key we are comparing the actual data
    for key in data_from_json_file.keys():
        assert key in response_body
        assert response_body[key] == data_from_json_file[key]  # checking that the keys (firstname, lastname,additionalneeds) values (Luka, Doncic, LA Lakers) in the patch_file.json are same of the patch_response_body


def test_full_update_booking(request_context):
    """Update entire booking record"""
    # this is an example of url to send with path param =>  https://restful-booker.herokuapp.com/booking/5244

    user_home = Path.home()  # Get user home directory
    json_file_path = user_home / "PycharmProjects" / "PythonSelenium" / "_plywrg_API_PY" / "testdata" / "put_request_body.json"
    data_from_json_file = read_json(json_file_path)

    response = request_context.put(
        f"{base_url}/booking/{booking_id}",
        headers={"Cookie": f"token={token_generated}"},
        data=data_from_json_file,
    )
    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print(f"\nFull Update Response for booking {booking_id}:", response_body)

    # Validate that full booking details were updated correctly
    # with a loop:
    for key in data_from_json_file.keys():
        assert key in response_body
        assert response_body[key] == data_from_json_file[key]

    # or validation one by one:
    assert response_body["firstname"] == data_from_json_file["firstname"]
    assert response_body["lastname"] == data_from_json_file["lastname"]
    assert response_body["totalprice"] == data_from_json_file["totalprice"]
    assert response_body["additionalneeds"] == data_from_json_file["additionalneeds"]


# -------------------------------------------------------------------
# 6) Delete Booking (DELETE)
# -------------------------------------------------------------------
def test_delete_booking(request_context):
    """Delete booking using auth token"""
    response = request_context.delete(
        f"{base_url}/booking/{booking_id}",
        headers={"Cookie": f"token={token_generated}"}  # we need to pass only ID as path param and Token as header
    )

    # API returns 201 on successful deletion
    assert response.status == 201
    assert response.status_text=="Created"

    print(f"\nBooking deleted successfully - ID:", booking_id)

