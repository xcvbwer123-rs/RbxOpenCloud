class OpenCloudException(Exception): pass
class InvalidFile(OpenCloudException): pass
class RequestError(OpenCloudException): pass
class InvalidAsset(OpenCloudException): pass
class ModeratedText(OpenCloudException): pass
class InvalidKey(OpenCloudException): pass
class RateLimited(OpenCloudException): pass
class ServiceUnavailable(OpenCloudException): pass