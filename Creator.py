from . import Exceptions, Utils
from requests import Response
import urllib3
import os
import json

creatorTypes = {
    "User": "user",
    "Group": "group"
}

fileTypes = {
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg",
    "png": "image/png",
    "jpeg": "image/jpeg",
    "bmp": "image/bmp",
    "tga": "image/tga",
    "fbx": "model/fbx"
}

assetTypes = {
    "Decal": "Decal",
    "Audio": "Audio",
    "Model": "Model",
    "Unknown": "Unknown",
}

class __Operation():
    def __init__(self, apiResponse: Response, apiKey: str):
        try:
            self.operationId = apiResponse.json()["path"].split("/")[1]

            session = Utils.newSession(apiKey=apiKey)
            response = session.get(Utils.baseUrl+f"assets/v1/operations/{self.operationId}")

            if response.status_code == 400: raise Utils.InvalidAsset(f"The file is not a supported type, or is corrupted.")
            elif response.status_code == 401: raise Utils.InvalidKey("Your key may have expired, or may not have permission to access this resource. Checkout your api key's ip.")
            elif response.status_code >= 500: raise Utils.ServiceUnavailable("The service is unavailable or has encountered an error.")

            data = response.json()

            self.__session = session
            self.done = data.done
            self.assetId = data.response.assetId
            self.name = data.response.displayName
            self.description = data.response.description
            self.link = f"https://www.roblox.com/library/{self.assetId}"
        except Exception as e:
            raise Exceptions.OpenCloudException(f"Unexpected Error : {e}")
        
    def refresh(self):
        session = self.__session
        response = session.get(Utils.baseUrl+f"assets/v1/operations/{self.operationId}")

        if response.status_code == 400: raise Utils.InvalidAsset(f"The file is not a supported type, or is corrupted.")
        elif response.status_code == 401: raise Utils.InvalidKey("Your key may have expired, or may not have permission to access this resource. Checkout your api key's ip.")
        elif response.status_code >= 500: raise Utils.ServiceUnavailable("The service is unavailable or has encountered an error.")

        data = response.json()

        self.done = data.done
        self.assetId = data.response.assetId
        self.name = data.response.displayName
        self.description = data.response.description
        self.link = f"https://www.roblox.com/library/{self.assetId}"



class Asset():
    def __init__(self, filePath: str, assetType: str):
        if os.path.exists(filePath):
            with open(filePath, "rb") as file:
                self.fileObject = (file.name, file.read(), fileTypes.get(file.name.split(".")[-1]))
        else:
            raise Exceptions.InvalidFile(f"File : \"{filePath}\" does not exist.")
        
        self.assetType = assetType


class Creator():
    def __init__(self, creatorType: str, creatorId: int, apiKey: str=None):
        self.creatorType = creatorType.lower()
        self.creatorId = str(creatorId)
        self.apiKey = apiKey or Utils.getApiKey()

    def upload(self, asset: Asset, name: str, description: str, price: int=None):
        data, contentType = urllib3.encode_multipart_formdata({
            "request": json.dumps({
                "assetType": asset.assetType,
                "creationContext": {
                    "creator": {
                        f"{self.creatorType}Id": self.creatorId
                    },
                    "expectedPrice": price or 0
                },
                "displayName": name,
                "description": description
            }),
            "fileContent": asset.fileObject
        })

        session = Utils.newSession({"content-type": contentType}, self.apiKey)
        response = session.post(Utils.baseUrl+"assets/v1/assets", data=data)

        if response.status_code == 400 and response.json()["message"] == "\"InvalidImage\"": raise Utils.InvalidAsset(f"The file is not a supported type, or is corrupted.")
        elif response.status_code == 400 and response.json()["message"] == "AssetName is moderated.": raise Utils.ModeratedText(f"The asset's name was moderated.")
        elif response.status_code == 400 and response.json()["message"] == "AssetDescription is moderated.": raise Utils.ModeratedText(f"The asset's description was moderated.")
        elif response.status_code == 401 or response.status_code == 403: raise Utils.InvalidKey("Your key may have expired, or may not have permission to access this resource. Checkout your api key's ip.")
        elif response.status_code == 429: raise Utils.RateLimited("You're being rate limited.")
        elif response.status_code >= 500: raise Utils.ServiceUnavailable("The service is unavailable or has encountered an error.")
        elif not response.ok: raise Utils.OpenCloudException(f"Unexpected HTTP {response.status_code}")

        return __Operation(response, self.apiKey)
    
    def update(self, assetId: int, asset: Asset):
        data, contentType = urllib3.encode_multipart_formdata({
            "request": json.dumps({
                "assetId": assetId
            }),
            "fileContent": asset.fileObject
        })

        session = Utils.newSession({"content-type": contentType}, self.apiKey)
        response = session.patch(Utils.baseUrl+f"assets/v1/assets/{assetId}", data=data)

        if response.status_code == 400 and response.json()["message"] == "\"InvalidImage\"": raise Utils.InvalidAsset(f"The file is not a supported type, or is corrupted.")
        elif response.status_code == 400 and response.json()["message"] == "AssetName is moderated.": raise Utils.ModeratedText(f"The asset's name was moderated.")
        elif response.status_code == 400 and response.json()["message"] == "AssetDescription is moderated.": raise Utils.ModeratedText(f"The asset's description was moderated.")
        elif response.status_code == 401 or response.status_code == 403: raise Utils.InvalidKey("Your key may have expired, or may not have permission to access this resource. Checkout your api key's ip.")
        elif response.status_code == 429: raise Utils.RateLimited("You're being rate limited.")
        elif response.status_code >= 500: raise Utils.ServiceUnavailable("The service is unavailable or has encountered an error.")
        elif not response.ok: raise Utils.OpenCloudException(f"Unexpected HTTP {response.status_code}")

        return __Operation(response, self.apiKey)