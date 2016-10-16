# REST Client for the Qualys SSL Labs Server Test

## Dependencies
Requests: http://docs.python-requests.org/en/lates/

## Usage

Initialize an instance of the REST Client

```
In[2]: from ssllabs.clients import RESTClient
In[3]: hostname = "www.ssllabs.com"
In[4]: client = RESTClient(host=hostname)
```

Now, you can call the API endpoints:

### info

```
In[5]: response = client.info()
In[6]: response
Out[6]: 

{u'clientMaxAssessments': 25,
 u'criteriaVersion': u'2009l',
 u'currentAssessments': 0,
 u'engineVersion': u'1.24.0',
 u'maxAssessments': 25,
 u'messages': [u'This assessment service is provided free of charge by Qualys SSL Labs, subject to our terms and conditions: https://www.ssllabs.com/about/terms.html'],
 u'newAssessmentCoolOff': 1000}
```

### getEndpointData

```
In[7]: response = client.get_endpoint_data(s='173.203.82.166')
In[8]: response
Out[8]: 
{u'errors': [{u'message': u'Endpoint not found'}]}
```

### analyze

```
response = client.analyze()
```

By default, analyze will start a new assessment, you may choose to get cached results
```
response = client.analyze(from_cache='on')
```
