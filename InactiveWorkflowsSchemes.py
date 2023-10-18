#This scripts list all inactive workflows schemes

import requests
from requests.auth import HTTPBasicAuth
import json
# importing the domain, the username and the API Token
import environment

def projectsIDs():


    # setting hearders and builiding the GET request
    url = "https://"+ environment.domain + ".atlassian.net/rest/api/3/project/search?maxResults=50&startAt=0"

    auth = HTTPBasicAuth(environment.username, environment.token)
    
    # Array that will store all project IDs
    projectids = []

    headers = {
      "Accept": "application/json"
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       auth=auth
    )

    # converting the GET request response into a dict 
    result = json.loads(response.text)
    
    #populating the array with the project IDs
    for values in result['values']:
      projectids.append(values['id']) 
    
    # Checking if the GET response returns a next page, if yes then perform a new call starting from the point mentioned in the nextPage key value
    while 'nextPage' in result:
      url = result['nextPage']
      
      response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
      )
      
      result = json.loads(response.text)
      for values in result['values']:
        projectids.append(values['id'])
   
    # return the array with all projectids in the Jira instance    
    return(projectids)
      
        
def checkInactiveWorkflows(projectids):
  
  workflowsids = []
  
  url = "https://"+ environment.domain + ".atlassian.net/rest/api/2/workflowscheme/project"

  auth = HTTPBasicAuth(environment.username, environment.token)
  
  headers = {
    "Accept": "application/json"
  }
  
  
  for id in projectids:
    #"'%s'" % id 
    query = {
      'projectId': id
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=query,
       auth=auth
    )
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    result = json.loads(response.text)
    
    for values in result['values']:
      workflowsids.append(values['workflowScheme']['id']) 
    
  print(workflowsids)

ids = projectsIDs()
checkInactiveWorkflows(ids)
