import requests
from . import Exceptions

baseUrl = "https://apis.roblox.com/"
apiKey = ""

def setApiKey(key: str):
    global apiKey

    apiKey = key
    
def getApiKey():
    global apiKey

    return apiKey

def newSession(headers=None, apiKey: str=None):
    session = requests.session()
    if apiKey:
        session.headers.update({"x-api-key": apiKey})
    elif len(getApiKey()) > 0:
        session.headers.update({"x-api-key": apiKey})
    else:
        raise Exceptions.RequestError("Api Key missing or invalid.")
    
    if headers:
        session.headers.update(headers)

    return session