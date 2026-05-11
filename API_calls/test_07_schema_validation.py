"""
Pre-requisites:
----------------
Install dependencies
    pip install jsonschema

"""
from jsonschema import validate, ValidationError
from playwright.sync_api import sync_playwright, Playwright

# Helper function to validate schema
def validate_json_schema(response_json,myschema):
    try:
        validate(instance=response_json,schema=myschema)  # this validate method will validate is response_body follows the schema
        print("Schema validation succcessfull..")
        return True
    except ValidationError as e:
        print("Schema validation failed")
        return False



def test_validate_json_schema_one(playwright:Playwright):
    request_context = playwright.request.new_context(
        ignore_https_errors=True  # 🔧 This fixes the SSL issue --> unable to get local issuer certificate
    )

    response=request_context.get("https://mocktarget.apigee.net/json")

    assert response.ok
    response_body=response.json()  # we got to validate the BODY OF THE RESPONSE with the schema . This body must follow the schema

    print(response_body)

    # schema ( Generated from the tool https://transform.tools/json-to-json-schema)
    schema = {          # --> in this way we are hardcoding the schema
        "type": "object",
        "properties": {
            "firstName": {
                "type": "string"
            },
            "lastName": {
                "type": "string"
            },
            "city": {
                "type": "string"
            },
            "state": {
                "type": "string"
            }
        },
        "required": [
            "firstName",
            "lastName",
            "city",
            "state"
        ]
    }

    is_valid = validate_json_schema(response_body, schema)  # let's call the function
    assert is_valid

    request_context.dispose()



def test_validate_json_schema_two(playwright:Playwright):
    request_context = playwright.request.new_context()

    response=request_context.get("https://jsonplaceholder.typicode.com/posts/1")


    is_valid=validate_json_schema
    assert response.ok
    response_body=response.json()

    print(response_body)

    # schema ( Generated from teh tool https://transform.tools/json-to-json-schema)
    schema = {
        "title": "Generated schema for Root",
        "type": "object",
        "properties": {
            "userId": {
                "type": "number"
            },
            "id": {
                "type": "number"
            },
            "title": {
                "type": "string"
            },
            "body": {
                "type": "string"
            }
        },
        "required": [
            "userId",
            "id",
            "title",
            "body"
        ]
    }

    is_valid=validate_json_schema(response_body,schema)
    assert is_valid

    request_context.dispose()



