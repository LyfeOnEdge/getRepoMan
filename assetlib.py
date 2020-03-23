import json

ICON_NAME = "icon.png"
SCREENSHOT_NAME = "screen.png"

ASSET = {
	"url": "",
	"dest": "",
	"type": ""
}

SCREENSHOT = {
	"url": "screen.png",
	"type": "screenshot"
}

ICON = {
	"url": "icon.png",
	"type": "icon"
}

ZIP = {
	"url": "",
	"type": "zip",
	"zip": []
}

ZIP_ASSET = {
	"path": "",
	"dest": "",
	"type": ""
}

NORMAL_ASSET_TYPE_LIST = {
	"update",
	"get",
	"local",
	"extract",
}

ASSET_TYPES = [
	"screenshot",
	"icon",
	"zip",
]


class baseAsset:
	def __init__(self, asset: dict):
		self.asset = asset
	def __repr__(self):
		return(self)
	def __str__(self):
		return json.dumps(self.asset, indent = 4)
	def to_string(self):
		return self.__str__()
	@property
	def type(self):
		print(self.asset)
		return self.asset["type"]
	@property
	def url(self):
		return self.asset.get("url") or self.asset.get("path")
	@property
	def subassets(self):
		return []
	def get(self):
		return self.asset

class Asset(baseAsset):
	def __init__(self, asset):
		baseAsset.__init__(self, asset)

class emptyAsset(Asset):
	def __init__(self):
		Asset.__init__(self, ASSET)

class imageAsset(baseAsset):
	def __init__(self, asset):
		baseAsset.__init__(self, asset)

class screenshotAsset(imageAsset):
	def __init__(self, asset):
		imageAsset.__init__(self, asset)

class localScreenshotAsset(screenshotAsset):
	def __init__(self):
		screenshotAsset.__init__(self, SCREENSHOT)

class iconAsset(imageAsset):
	def __init__(self, asset):
		imageAsset.__init__(self, asset)

class localIconAsset(iconAsset):
	def __init__(self):
		iconAsset.__init__(self, ICON)

class zipAsset(baseAsset):
	def __init__(self, asset):
		baseAsset.__init__(self, asset)
		self.subassetslist = []
		self.factory()

	@property
	def subassets(self):
		return self.subassetslist

	# def __str__(self):
	# 	return json.dumps(self.asset, indent = 4)

	def factory(self):
		for asset in self.asset["zip"]:
			self.add_asset(asset)

	def add_asset(self, asset):
		self.subassetslist.append(Asset(asset))

	#Clears list of loaded assets
	def clear_asset(self):
		self.subassetslist = []

	

class emptyZipAsset(zipAsset):
	def __init__(self):
		zipAsset.__init__(self, ZIP)

ASSET_TYPE_MAP = {
	"screenshot" : screenshotAsset,
	"icon" : iconAsset,
	"zip" : zipAsset,
}

def asset_factory(assets: list):
	asset_object_list = []
	for asset in assets:
		if asset["type"] in NORMAL_ASSET_TYPE_LIST:
			asset_object_list.append(Asset(asset))
			continue
		if asset["type"] in ASSET_TYPES:
			asset_object_list.append(ASSET_TYPE_MAP[asset["type"]](asset))
			continue
		print(f"Failed to process {asset}")
	return asset_object_list

