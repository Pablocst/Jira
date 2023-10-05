# Create Jira users from a CSV file. 
import requests
import sys
from requests.auth import HTTPBasicAuth
import json

url = "https://palbuquerque.atlassian.net/rest/api/3/user"

auth = HTTPBasicAuth("palbuquerque@atlassian.com", "ATATT3xFfGF0FLxYt4pgiI0CbDD7hvEUF-97-Bke-77B4_MIvzGDE5HupphMdM-UcesrCFnnJXsB7BFd0gfcpjxCRc5Frc7pej8C2A6WtMQ6Lh4SdzyAiYh1M8oqDZgdGmlkswCXqkEPKIynMPsNBZFNjg_ceHQTD5J05Stlpu3PwwJ2F2Q5Im8=9FAC86E9")

with open(sys.argv[1], 'r') as f:
    csvfile = f.readlines()
    
for line in csvfile:
     user_mail_address = line.strip().split(",")[1]
    
     headers = {
     "Accept": "application/json",
     "Content-Type": "application/json"
     }
     payload = json.dumps( {
     "emailAddress": f"{user_mail_address}"
     } )
     response = requests.request(
     "POST",
     url,
     data=payload,
     headers=headers,
     auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


