from flask import Flask,redirect,request
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv 

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')
redirect_uri = os.getenv('REDIRECT_URI');
scope = os.getenv('SCOPE');
state = os.getenv('STATE');
access_token = ""
personID = ""
# access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
# api_url_base = 'https://api.linkedin.com/v2/'
# urn = os.getenv('LINKEDIN_URN')
# author = f"urn:li:person:{urn}"
# headers = {'X-Restli-Protocol-Version': '2.0.0',
#            'Content-Type': 'application/json',
#            'Authorization': f'Bearer {access_token}'}



#Simple post share
def simple_post(person_id,visibility,post_text):
    api_url = f'{api_url_base}ugcPosts'

    post_data = {
        "author": f"urn:li:person:{person_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE"
            },
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": visibility
        },
    }

    response = requests.post(api_url, headers=headers, json=post_data)

    if response.status_code == 201:
        print("Success")
        print(response.content)
    else:
        print(response.content)

#article share
def article_post(person_id,visibility,post_text,link_title,link_desc,link_url):
    api_url = f'{api_url_base}ugcPosts'

    post_data = {
        "author": f"urn:li:person:{person_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": link_desc
                        },
                        "originalUrl": link_url,
                        "title": {
                            "text": link_title
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": visibility
        }
    }

    response = requests.post(api_url, headers=headers, json=post_data)

    if response.status_code == 201:
        print("Success")
        print(response.content)
    else:
        print(response.content)

#Image share 
def registerUploadRequest(person_id):
    api_url = f'{api_url_base}assets?action=registerUpload'

    registerUploadRequest = {
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "owner": f"urn:li:person:{person_id}",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }
    response = requests.post(api_url, headers=headers,json=registerUploadRequest)
    if response.status_code == 200:
        print("registerUploadRequest succeed")
        res = response.json()
        # Upload your image to LinkedIn
        uploadUrl = res['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        uploadImage(uploadUrl)
        return res
    else:
        print("RegisterUploadRequest failed")
        return ""

def uploadImage(uploadUrl,file):
    files = open("images/image.jpg" ,"rb").read()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.put(uploadUrl, data=files, headers=headers)
    if response.status_code == 201:
        print("Image Uploaded")
    else:
        print("Image upload failed")

def image_post(person_id,post_text,image_title,image_desc):
    api_url = f'{api_url_base}ugcPosts'
    register_resp=registerUploadRequest()
    if(register_resp!=""):
        post_data = {
            "author": f"urn:li:person:{person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                    "text": post_text                    
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": image_desc
                            },
                            "media": register_resp['value']['asset'],
                            "title": {
                                "text": image_title
                            }
                        }
                    ]
                },
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
            },
        }

        response = requests.post(api_url, headers=headers, json=post_data)

        if response.status_code == 201:
            print("Posted Successfully")
    else:
        print("Post unsuccessful")
        
@app.route('/')
def homepage():
    return 'Linked Automation'

@app.route('/getAuthUrl')
def getAuthUrl():
    url = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=" + app_id + "&redirect_uri="+ redirect_uri + "&scope=" + scope + "&state" + state;
    return redirect(url)

@app.route('/callback')
def getAccessToken():
    code = request.args.get("code")
    url = "https://www.linkedin.com/oauth/v2/accessToken?"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params={"client_id":app_id,"client_secret":app_secret,"grant_type":"authorization_code","redirect_uri":redirect_uri,"code":code}
    response = requests.post(url, params=params, headers=headers)
    if response.status_code == 200:
        res = response.json()
        global access_token
        access_token = res['access_token']
        return redirect("/getPersonID")
    else:
        return "Authentication failed.Relogin"
    return redirect(url)
    
@app.route('/getPersonID')
def getPersonID():
    url = "https://api.linkedin.com/v2/me"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params={"oauth2_access_token":access_token}
    response = requests.get(url, params=params, headers=headers)
    print (response.status_code)
    if response.status_code == 200:
        res = response.json()
        global personID
        personID = res['id']
        return personID
    else:
        return "Fetching userdetails failed"
    return redirect(url)

if __name__ == '__main__':
    app.run()