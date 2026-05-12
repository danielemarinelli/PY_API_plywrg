from playwright.sync_api import Playwright

#5) API Key Authentication - OpenWeatherMap
# https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
# API SWAGGER ====> https://openweathermap.org/api
def test_api_key_auth_openweather(playwright: Playwright):
#
     request_context = playwright.request.new_context()
#    city and Key auth is passed as query params
     query_params = {
         "q": "Urbino",
         "appid": "fc5811e51f0cfb52ac70c860eb0aefa7"
#
     }
     response = request_context.get("https://api.openweathermap.org/data/2.5/weather",
                                    params=query_params
                                        )

     assert response.status==200
     response_body=response.json()
#
     print("weather info:====>",response_body)


#6) API Key Authentication - weatherAPI
# URL: https://api.weatherapi.com/v1/current.json

# def test_api_key_auth_weatherapi(playwright: Playwright):
#
#     request_context = playwright.request.new_context()
#
#     query_params = {
#         "q": "Buffalo",
#         "key": "59f38ebe55d5436ca0552856250606"
#
#     }
#     response = request_context.get("https://api.weatherapi.com/v1/current.json",
#                                    params=query_params
#                                        )
#     assert response.status==200
#     response_body=response.json()
#
#     print("weather info:====>",response_body)