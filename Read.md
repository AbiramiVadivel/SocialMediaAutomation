# Social-Media-Automation 

##LinkedIn 
Python bot to post on LinkedIn profile via LinkedIn API.

### Steps to run script 
create virtual environmnet to prevant dependancy conflict
1. Install the requirements using pip as `pip install -r requirements.txt`.
2. Create an app on LinkedIn's developers account [here](https://www.linkedin.com/developers/) and follow the guide [here](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?context=linkedin/context) to get the access token. 
3. Post access token, send a `GET` request defined [here](https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin?context=linkedin/consumer/context#api-request) to get the Person `URN'.
3. Create a `.env` file and copy below text.
```
ACCESS_TOKEN="<your access token>"
URN="<your urn>"
```
4. Run the script using `python linkedin.py` which will print the `SUCCESS` and `id` of the post shared as a JSON response. You can check on your LinkedIn profile.
