if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		print(path.dirname( path.dirname( path.abspath(__file__) ) ))
		sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
		from openCloud import Utils, Creator
	else:
		from . import Utils, Creator

Utils.setApiKey("w2ATTEfKd0+KCB6BTgsid+9gF9i15dw0F+tU4WcFzZMcS2zL")

Asset = Creator.Asset("C:/Users/배려/Downloads/studio.png", "Decal")
Creator = Creator.Creator("user", 361208413)

Creator.upload(Asset, "Purple Studio Icon", "Decal")

print(__name__)