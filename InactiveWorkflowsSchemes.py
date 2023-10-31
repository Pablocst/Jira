#This script lists all inactive workflow schemes

import requests
from requests.auth import HTTPBasicAuth
import json
# Importing the domain, the username and the API Token
import environment
# 

def projectsIDs():


    # setting headers and building the GET request
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
      
#Get a list of all active workflows
       
def checkActiveWorkflows(projectids):
  
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
  
  workflowsids = set(workflowsids)
  workflowsids = list(workflowsids)  
  return(workflowsids)

def checkInactiveWorkflows(activeworkflowsids):
  
  workflowsids = []
  url = "https://"+ environment.domain + ".atlassian.net/rest/api/2/workflowscheme?maxResults=50&startAt=0"
  auth = HTTPBasicAuth(environment.username, environment.token)
    
  # Array that will store all inactive workflows IDs
  inactiveworkflowsids = []
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
  
  #populating the array with the workflows IDs
  for values in result['values']:
    workflowsids.append(values['id']) 
  
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
      workflowsids.append(values['id'])
  
  # Get the difference between all Workflows Schemes and the active ones, this will result in the Inactive ones
  
  for ids in workflowsids:
      if (ids not in activeworkflowsids):
        inactiveworkflowsids.append(ids)
    
    
        
  return(inactiveworkflowsids)


ids = projectsIDs()
activeworkflowsids = checkActiveWorkflows(ids)
inactiveworkflowsids = checkInactiveWorkflows(activeworkflowsids)
print("Inacctive Workflows Schemes", inactiveworkflowsids)
