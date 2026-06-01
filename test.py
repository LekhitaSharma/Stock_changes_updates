import requests
from requests.auth import HTTPBasicAuth

account_sid = "AC3edbfa8eb05a4376a7ebe2a54fec1310" # paste here
auth_token = "4d5302bf5bb37eefa75f3f72687bd6ec" # paste here

print("SID repr:", repr(account_sid))
print("Token length:", len(auth_token))

url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}.json"
r = requests.get(url, auth=HTTPBasicAuth(account_sid, auth_token))

print("HTTP:", r.status_code)
print(r.text[:300])