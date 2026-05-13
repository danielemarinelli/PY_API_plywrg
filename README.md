Step 1) Run single below command to install all the required plugins: pip install pytest playwright pytest-xdist pytest-html allure-pytest pytest-rerunfailures openpyxl Faker python-slugify

Step 2) Install pytest playwright: pip install pytest-playwright

TWO APIs are implemented in this framework:

########## API Booking under folder API_calls ###################

Run tests with command line ===> pytest API_calls

uncomment the tests to run based on the groups configured in pytest.ini 

Follow the Swagger pdf attached as documentation

for test_09 bearer token must be generated for lines 9 and 26 ( if  expired)


########## API Map Place under folder RSA_GoogleMaps ###################

it's an e2e CRUD flow in file test_11_e2e_GoogleMaps.py

follow the documentation ==> Swagger-PlaceAPIs.docx

run command ==> pytest RSA_GoogleMaps/

execution will follow the pytest.ini configuration (if grouping marker end_to_end is commented, the test won't execute) 

