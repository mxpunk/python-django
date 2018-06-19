#!/usr/bin/python

import cgi, ssl, urllib3, requests, ldap3, kerberos, json, sys, os
from requests_ntlm import HttpNtlmAuth

myjson = json.loads(sys.stdin.read())
if myjson['event'] == "verification":
    sys.stdout.write("Status: 200 OK\n")
    sys.stdout.write("Content-Type: text/plain\n")
    sys.stdout.write("\n")
    sys.stdout.write("Work")
else:
    if os.getenv("QUERY_STRING") in ('iOS', 'Android'):
      sys.stdout.write("Status: 200 OK\n")
      sys.stdout.write("Content-Type: text/plain\n")
      sys.stdout.write("\n")
      sys.stdout.write("Work")
      headers={'content-type': 'application/json-patch+json'}
      urlget = 'https://tfs.domain.local/tfs/DefaultCollection/Messenger/_apis/work/teamsettings/iterations?$timeframe=current&api-version=v2.0-preview'
      getres = requests.get(urlget,headers=headers,auth=HttpNtlmAuth('domain\\ADuserfabric','password'),verify=False).json()
      url = 'https://tfs.sbr.local/tfs/DefaultCollection/Messenger/_apis/wit/workitems/$Bug?api-version=2.0'
      if os.getenv("QUERY_STRING") in ('Android'):
        personis = 'Second programmer name <DOMAIN\\ADNameFirstProgrammer>'
      if os.getenv("QUERY_STRING") in ('iOS'):
        personis = 'Second programmer name <DOMAIN\\ADNameSecondProgrammer>'
      uploadjson = [
          {
            'op': 'add',
            'path': '/fields/System.AreaPath',
            'value': 'Messenger\\Front\\'+os.getenv("QUERY_STRING")
          },
          {
            'op': 'add',
            'path': '/fields/System.TeamProject',
            'value': 'Messenger'
          },
          {
            'op': 'add',
            'path': '/fields/System.IterationPath',
            'value': getres['value'][0]['path']
          },
          {
            'op': 'add',
            'path': '/fields/System.WorkItemType',
            'value': 'Bug'
          },
          {
            'op': 'add',
            'path': '/fields/State',
            'value': 'New'
          },
          {
            'op': 'add',
            'path': '/fields/System.Reason',
            'value': 'Fabric'
          },
          { 
            'op': 'add',
            'path': '/fields/System.AssignedTo',
            'value': 'None',
            'value': personis
          },
          {
            'op': 'add',
            'path': '/fields/Microsoft.VSTS.Scheduling.OriginalEstimate',
            'value': 1.0
          },
          {
            'op': 'add',
            'path': '/fields/Microsoft.VSTS.Scheduling.RemainingWork',
            'value': 1.0
          },
          {
            'op': 'add',
            'path': '/fields/Microsoft.VSTS.TCM.ReproSteps',
            'value': "<a href="+myjson['payload']['url']+">"+myjson['payload']['url']+"</a>"
          },
          {
            'op': 'add',
            'path': '/fields/Microsoft.VSTS.Build.FoundIn',
            'value': '<None>'
          },
          {
            'op': 'add',
            'path': '/fields/System.Title',
            'value': myjson['payload']['title']
          }
          ]
    res = requests.patch(url,json=uploadjson,headers=headers,auth=HttpNtlmAuth('domain\\ADuserfabric','password'),verify=False)
