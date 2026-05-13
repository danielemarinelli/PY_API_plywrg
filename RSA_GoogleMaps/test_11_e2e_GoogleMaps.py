import json
from playwright.sync_api import Playwright
import pytest


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

# common for all RESTful calls
mandatory_key = "qaclick123"
base_url = "https://rahulshettyacademy.com"


# -------------------------------------------------------------------
# Test: Create e2e flow for adding a place, retrieve it, update it and delete it
# Request Type: POST, GET, PUT, DELETE
# -------------------------------------------------------------------


@pytest.mark.end_to_end
def test_create_place(request_context):

    # Load request body from external JSON file or (not best practice) hardcoded data
    #file = open("testdata/post_body_api_maps.json", "r")
    #request_body =  json.load(file)
    global request_body
    request_body = { #json.load(file)
        "location": {
            "lat": -48.383494,
            "lng": 63.427362
        },
        "accuracy": 50,
        "name": "Holiday Circle",
        "phone_number": "(+39) 344 893 3900",
        "address": "280, side line avenue, Buffalo",
        "types": [
            "flag football",
            "F_NFL"
        ],
        "website": "http://f_nfl.com",
        "language": "Spanish"
    }


    # Send POST request with payload as body
    response = request_context.post(f"{base_url}/maps/api/place/add/json", data=request_body, params=mandatory_key)

    # Extract response body
    response_body = response.json()
    print(response_body)

    '''
    EXAMPLE OF HOW A RESPONSE BODY IS:
   {
    "status": "OK",
    "place_id": "996fd647d1d126f66f9a5be6837c8421",
    "scope": "APP",
    "reference": "576215384b8a4e07e665c135da92c968576215384b8a4e07e665c135da92c968",
    "id": "576215384b8a4e07e665c135da92c968"
    }
    '''

    # ------------------------------
    # Validations
    # ------------------------------
    assert response.ok
    assert response.status == 200

    # Validate top-level keys of the response
    assert "id" in response_body
    assert "status" in response_body
    assert "scope" in response_body
    assert "reference" in response_body
    assert "place_id" in response_body


    # Validate booking details
    assert response_body["status"] == "OK"
    assert response_body["scope"] == "APP"

    # Store place ID and other values globally for reuse in subsequent tests
    global place_id
    place_id = response_body["place_id"]
    print("=============>",place_id)

    # ------------GET---------------------------------------------
@pytest.mark.end_to_end
def test_get_place_by_id(request_context):
    """Get booking details using booking ID"""
    # Send GET request

    response = request_context.get(f"{base_url}/maps/api/place/get/json",
                                   params={     # two or more query params must be passed with a dictionary
                                        "place_id": place_id,
                                        "key": mandatory_key
                                        }
                                   )

    # Extract response body
    response_body = response.json()
    print(response_body)

    ''' The example of GET RESPONSE:
    {
    "location": {
        "latitude": "-48.383494",
        "longitude": "63.427362"
    },
    "accuracy": "50",
    "name": "Holiday Circle",
    "phone_number": "(+39) 344 893 3900",
    "address": "280, side line avenue, Buffalo",
    "types": "flag football,F_NFL",
    "website": "http://f_nfl.com",
    "language": "Spanish"
}
    
    '''

    # Validate presence of expected fields
    assert "name" in response_body
    assert "accuracy" in response_body
    assert "phone_number" in response_body
    assert "address" in response_body
    assert "types" in response_body
    assert "website" in response_body
    assert "language" in response_body
    assert "location" in response_body

    assert response_body["name"] == request_body["name"]
    assert response_body["phone_number"] == request_body["phone_number"]
    assert response_body["address"] == request_body["address"]
    assert response_body["website"] == request_body["website"]
    assert response_body["language"] == request_body["language"]
    #assert response_body["location"]["latitude"] == request_body["location"]["latitude"]
    #assert response_body["location"]["longitude"] == request_body["location"]["longitude"]




    # ------------PUT---------------------------------------------
@pytest.mark.end_to_end
def test_update_address_place(request_context):
    """Update address place using place ID"""
    # Send PUT request
    global request_update_body   # global variable to use for test test_get_updated_place()
    request_update_body = {  # json.load(file)

        "place_id":place_id,
        "address":"78 Summer walk, Urbino Italy",
        "key":"qaclick123"

    }

    # Send PUT request with payload as body
    response = request_context.put(f"{base_url}/maps/api/place/update/json", data=request_update_body, params=mandatory_key)

    # Extract response body
    '''
    {
    "msg": "Address successfully updated"
    }
    '''
    response_update_body = response.json()
    print(response_update_body)

    # Validate presence of expected fields
    assert "msg" in response_update_body
    assert response_update_body["msg"] == "Address successfully updated"

# ------------GET call with updated address---------------------------------------------
@pytest.mark.end_to_end
def test_get_updated_place(request_context):
        """Get booking details using booking ID"""
        # Send GET request

        response = request_context.get(f"{base_url}/maps/api/place/get/json",
                                       params={  # two or more query params must be passed with a dictionary
                                           "place_id": place_id,
                                           "key": mandatory_key
                                       }
                                       )

        # Extract response body
        new_response_body = response.json()
        print(new_response_body)
        assert new_response_body["address"] == request_update_body["address"]

# ------------DELETE---------------------------------------------
@pytest.mark.end_to_end
def test_delete_place_by_id(request_context):
        """Update address place using place ID"""
        # Send DELETE request with body
        request_delete_body = {  # json.load(file)

            "place_id": place_id

        }

        # Send DELETE request with payload as body
        response = request_context.put(f"{base_url}/maps/api/place/delete/json", data=request_delete_body,
                                           params=mandatory_key)

        # Extract response body
        '''
        {
        "status": "OK"
        }
        '''
        response_delete_body = response.json()
        print(response_delete_body)

        # Validate presence of expected fields
        assert "status" in response_delete_body
        assert response_delete_body["status"] == "OK"

        # Close the API context
        request_context.dispose()