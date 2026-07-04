import json
import requests
from google.auth import default
from google.auth.transport.requests import Request

# get default credentials and access token
creds, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds.refresh(Request())
access_token = creds.token

# api endpoint for session creation
url_session = "https://us-central1-aiplatform.googleapis.com/v1/projects/project-199286d8-f77c-45e7-bce/locations/us-central1/reasoningEngines/448264843330322432:query"

# payload for session creation
payload_session = {
    "class_method":"create_session",
    "input":{
        "user_id":"testId"
    }
}

# header
headers = {
    "Authorization":f"Bearer {access_token}",
    "Content-Type":"application/json"
}

# post request
response = requests.post(url_session, headers=headers, data=json.dumps(payload_session))

if response.status_code == 200:
  data=response.json()
  session_id=data["output"]["id"]
  print(f"Session created successfully! Session ID: {session_id}")
else:
  print(f"Request failed ({response.status_code}):")
  print(response.text)

payload_query={
    "class_method":"async_stream_query",
    "input":{
        "user_id":"testId",
        "session_id":session_id,
        "message":"Tell me about world war 2"
    }
}

url_query="https://us-central1-aiplatform.googleapis.com/v1/projects/project-199286d8-f77c-45e7-bce/locations/us-central1/reasoningEngines/448264843330322432:streamQuery?alt=sse"

response=requests.post(url_query, headers=headers, data=json.dumps(payload_query))
import json
data=json.loads(response.text)

# extract the text safely
text = data.get("content", {}).get("parts", [{}])[0].get("text","")

print("\nAgent Response: \n")
print(text)
