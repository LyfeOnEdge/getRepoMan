from gui.widgets import basePage, themedListbox, themedLabel, themedFrame, searchBox, scrollingWidgets
import platform, json
import tkinter as tk
from asyncthreader import threader
import style
from .assetlib import asset_factory
# emptyAsset, screenshotAsset, localScreenshotAsset, iconAsset, localIconAsset, zipAsset, emptyZipAsset

SIDECOLUMNWIDTH = 200

class AssetEditor(themedFrame.ThemedFrame):
	def __init__(self, container, package, exit_callback):
		themedFrame.ThemedFrame.__init__(self, container)
		self.place(relwidth = 1, relheight = 1)
		self.tkraise()
		self.original_package = package.copy()
		self.package = package
		self.assets = []

		self.left_column = themedFrame.ThemedFrame(self, background = style.primary_color)
		self.left_column.place(relheight = 1, width = SIDECOLUMNWIDTH)

		self.column_header = themedLabel.ThemedLabel(self.left_column, text = "ASSETS", font = style.mediumboldtext, foreground = style.primary_text_color)
		self.column_header.place(y = + style.offset, x = + style.offset, relwidth = 1, width = style.offset)

		self.left_column_listboxes = themedFrame.ThemedFrame(self.left_column, background = style.primary_color)
		self.left_column_listboxes.place(y = 30, relheight = 1, relwidth = 1, height = - 60)

		self.assetsindexlist = scrollingWidgets.ScrolledThemedListBox(self.left_column_listboxes, background = style.primary_color)
		self.assetsindexlist.place(relheight = 1, width = 20, x = + 2 * style.offset)

		self.assetstypelist = scrollingWidgets.ScrolledThemedListBox(self.left_column_listboxes, background = style.primary_color)
		self.assetstypelist.place(relheight = 1, relwidth = 1, x = 20 + 2 * style.offset, width = -(20 + 4 * style.offset))

		bindlist = [self.assetsindexlist, self.assetstypelist]
		if platform.system() == 'Windows' or platform.system() == "Darwin":
			for b in bindlist:
				b.bind("<MouseWheel>", self.on_mouse_wheel)
		elif platform.system() == "Linux":
			for b in bindlist:
				b.bind("<Button-4>", self.on_mouse_wheel)
				b.bind("<Button-5>", self.on_mouse_wheel)   

		self.body = themedFrame.ThemedFrame(self, background = style.secondary_color)
		self.body.place(relwidth = 1, relheight = 1, x = SIDECOLUMNWIDTH, width = SIDECOLUMNWIDTH)

		self.load()

		self.assetstypelist.bind("<<ListboxSelect>>", self.on_listbox_selection)

	def load(self):
		self.assets = asset_factory(self.package["assets"])

		self.assetsindexlist.configure(state = "normal")
		self.assetstypelist.configure(state = "normal")
		i = 1
		self.asset_index_map = {}
		for asset in self.assets:
			self.asset_index_map[i] = asset
			self.assetsindexlist.insert("end", i)
			self.assetstypelist.insert("end", asset.type)
			i += 1
		self.assetsindexlist.configure(state = "disable")

	def on_listbox_selection(self, event):
		selection=int(self.assetstypelist.curselection()[0]) + 1
		self.edit_asset(self.asset_index_map[selection])

	def edit_asset(self, asset):
		print(asset)


	def on_mouse_wheel(self, event):
		try:
			if platform.system() == 'Windows':
				self.assetstypelist.yview("scroll", int(-1*(event.delta/120),"units"))
			elif platform.system() == "Linux":
				if event.num == 5:
					self.assetstypelist.yview("scroll", 1,"units")
				if event.num == 4:
					self.assetstypelist.yview("scroll", -1,"units")
			elif platform.system() == "Darwin":
				self.assetstypelist.yview("scroll", event.delta,"units")

			assetsindexlist.yview_moveto(self.assetstypelist.yview()[0])

			return "break"
		except:
			pass