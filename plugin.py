from gui.widgets import basePlugin
from .page import Page
from .repoman import RepoHandler
from .pkgbuildPage import PkgbuildPage

class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "PLUGIN_NAME", container)
		self.app = app
		self.container = container
		self.detail_page = PkgbuildPage(app)
		self.handler = RepoHandler()

	def get_pages(self):
		return [Page(self.app, self.container, self)]

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)