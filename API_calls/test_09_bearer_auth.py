from playwright.sync_api import Playwright

# 3) Bearer Token Authentication is used in GitHub , where gets all your details repos
# url: https://api.github.com/user/repos

def test_bearer_token_auth_github_repos(playwright: Playwright):
     # to generate the token follow the steps:
     # a) Settings -> Developer Settings -> Personal access tokens -> Token (Classic) -> Generate new token
     #token="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"
     # token is passed always in headers and the response will contain all the repos details in JSON form
     request_context = playwright.request.new_context()
     response = request_context.get("https://api.github.com/user/repos",
                                        headers={"Authorization": f"Bearer {token}"}
                                       )
     assert response.status==200
     response_body=response.json()

     print("Response Body(Repositories....)",response_body)


# 4) Bearer Token Authentication
# url: https://api.github.com/user

def test_bearer_token_auth_github_user_info(playwright: Playwright):
     # returns the details of the user (same token as previous one)
     #token="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"

     request_context = playwright.request.new_context()
     response = request_context.get("https://api.github.com/user",
                                        headers={"Authorization": f"Bearer {token}"}
                                        )
     assert response.status==200
     response_body=response.json()

     print("Response Body(User details.....)",response_body)