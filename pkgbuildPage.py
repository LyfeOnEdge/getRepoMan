from gui.widgets import basePage, themedFrame, themedLabel, scrollingWidgets, themedEntry, button
from gui.detailPage import DetailPage
from asyncthreader import threader
from webhandler import opentab
import style
import json
from .assetEditor import AssetEditor
SIDEBAR_OFFSET = 25
EXCLUDED_SIDEBAR_KEYS = [
	"info",
	"details",
	"changelog",
	"assets",
	"description",
	"changes",
	"package"
]

class PkgbuildPage(DetailPage):
	def __init__(self, frame):
		DetailPage.__init__(self, frame)
		self.place(relwidth = 1, relheight = 1)
		#since page is dynamic, need a trash can
		self.frame = frame
		self.destroyables = []

		#Want to reuse a lot of the page but need to do some cleanup
		self.column_downloads.destroy()
		self.column_title.destroy()
		self.column_author.destroy()
		self.column_version.destroy()
		self.column_license.destroy()
		self.column_package.destroy()
		self.column_downloads.destroy()
		self.column_updated.destroy()
		self.column_uninstall_button.destroy()
		self.column_install_button.destroy()
		self.details.destroy()

		self.body.place(relwidth = 1, relheight = 1, width = - 2 * style.sidecolumnwidth)
		self.column.place(relx = 1, rely = 0, width = 2 * style.sidecolumnwidth, relheight = 1, x = - 2 * style.sidecolumnwidth)

		#Move buttons to be pretty
		self.column_open_url_button.place(rely=1,relwidth = 1, x = + 2 * style.offset, y = - 2 * (style.buttonsize + 2 * style.offset), width = - 4 * style.offset, height = style.buttonsize)
		self.column_backbutton.place(rely=1,relx=1,x = -(style.buttonsize + style.offset), y = -(style.buttonsize + 2 * style.offset))

		self.text_boxes_frame = themedFrame.ThemedFrame(self.body, background = style.secondary_color)
		self.text_boxes_frame.place(relwidth = 1, relheight = 1 - style.details_page_image_fraction, rely = style.details_page_image_fraction, x = 2 * style.offset, width = - 4 * style.offset, y = + 2 * style.offset, height = -4 * style.offset)

		description_label = themedLabel.ThemedLabel(self.text_boxes_frame, "Description:", anchor="w", font=style.smallboldtext, foreground = style.primary_text_color, background = style.secondary_color)
		description_label.place(relwidth = 1, height = 20)
		self.description = scrollingWidgets.ScrolledThemedText(self.text_boxes_frame, font = style.smalltext, foreground = style.detail_page_label_color)
		self.description.place(y = 20, relwidth = 1, height = 20)

		details_label = themedLabel.ThemedLabel(self.text_boxes_frame, "Details:", anchor="w", font=style.smallboldtext, foreground = style.primary_text_color, background = style.secondary_color)
		details_label.place(y = 40 + 2 * style.offset, relwidth = 1, height = 20)
		self.details = scrollingWidgets.ScrolledThemedText(self.text_boxes_frame, font = style.smalltext, foreground = style.detail_page_label_color)
		self.details.place(relheight = 0.75 ,y = 60 + 2 * style.offset, relwidth = 1, height = - (60 + 4 * style.offset))

		changes_label = themedLabel.ThemedLabel(self.text_boxes_frame, "Changelog:", anchor="w", font=style.smallboldtext, foreground = style.primary_text_color, background = style.secondary_color)
		changes_label.place(rely = 0.75, relwidth = 1, height = 20)
		self.changes = scrollingWidgets.ScrolledThemedText(self.text_boxes_frame, font = style.smalltext, foreground = style.detail_page_label_color)
		self.changes.place(relheight = 0.25, rely = 0.75, relwidth = 1, y = + 20, height = - 20)

		self.column_save_button = button.Button(self.column_body, 
			callback = self.save_json, 
			text_string = "SAVE", 
			font=style.mediumboldtext, 
			background=style.secondary_color
			)
		self.column_save_button.place(rely=1,relwidth = 1, x = + 2 * style.offset, y = - (style.buttonsize + 2 * style.offset), width = - (4 * style.offset + style.buttonsize), height = style.buttonsize)

		self.editor_button = button.Button(self.column_body, 
			callback = self.spawn_editor, 
			text_string = "ASSET EDITOR", 
			font=style.mediumboldtext, 
			background=style.secondary_color
			)
		self.editor_button.place(rely=1,relwidth = 1, x = + 2 * style.offset, y = - 3 * (style.buttonsize + 2 * style.offset), width = - (4 * style.offset), height = style.buttonsize)
		
	def spawn_editor(self):
		editor = AssetEditor(self.frame, self.package, None)

	def update_banner(self):
		self.bannerimage = self.appstore_handler.getScreenImage(self.package["package"])
		if self.bannerimage:
			self.do_update_banner(self.bannerimage)
		else:
			self.do_update_banner("gui/assets/notfound.png")

	def update_page(self, package):
		self.package = package

		threader.do_async(self.update_body)
		threader.do_async(self.build_sidebar)
		threader.do_async(self.update_banner)

	def update_body(self):
		package = self.package

		self.details.set_entry(package["info"]["details"].replace("\\n", """
"""))
		self.description.set_entry(package["info"]["description"].replace("\\n", """
"""))
		changes = (package["info"]["changelog"] if "changelog" in package["info"].keys() else (package["info"]["changes"] if "changes" in package["info"].keys() else ""))
		self.changes.set_entry(changes.replace("\\n", """
"""))

	def build_sidebar(self):
		package = self.package

		for w in self.destroyables:
			w.destroy()

		p = package["package"]
		w = themedLabel.ThemedLabel(self.column_body,
			f"Package - {p}",
			anchor="w",
			font=style.smallboldtext,
			foreground = style.primary_text_color,
			background = style.primary_color
		)
		w.place(
			x = style.offset,
			width = - style.offset,
			y = style.offset,
			relwidth = 1,
			height = SIDEBAR_OFFSET
		)
		self.destroyables.append(w)

		i = 1
		self.entries = {}
		for key in package.keys():
			if key in EXCLUDED_SIDEBAR_KEYS:
				continue

			w_l = themedLabel.ThemedLabel(self.column_body, key, anchor="w", font=style.smallboldtext, foreground = style.primary_text_color, background = style.primary_color)
			w_l.place(
				x = 2 * style.offset,
				y = i * (SIDEBAR_OFFSET + style.offset) + style.offset,
				relx = 0.0,
				relwidth = 0.20,
				height = SIDEBAR_OFFSET,
				width = - 4 * style.offset
			)

			w = themedEntry.ThemedEntry(self.column_body, font = style.smalltext)
			w.place(
				x = 2 * style.offset,
				y = i * (SIDEBAR_OFFSET + style.offset) + style.offset,
				relx = 0.20,
				relwidth = 0.80,
				height = SIDEBAR_OFFSET,
				width = - 4 * style.offset
			)
			w.set(package[key])
			self.entries[key] = w
			self.destroyables.extend([w,w_l])
			i += 1

		self.info_entries = {}
		for key in package["info"].keys():
			if key in EXCLUDED_SIDEBAR_KEYS:
				continue

			w_l = themedLabel.ThemedLabel(self.column_body, key, anchor="w", font=style.smallboldtext, foreground = style.primary_text_color, background = style.primary_color)
			w_l.place(
				x = 2 * style.offset,
				y = i * (SIDEBAR_OFFSET + style.offset) + style.offset,
				relx = 0.0,
				relwidth = 0.20,
				height = SIDEBAR_OFFSET,
				width = - 4 * style.offset
			)

			w = themedEntry.ThemedEntry(self.column_body, font = style.smalltext)
			w.place(
				x = 2 * style.offset,
				y = i * (SIDEBAR_OFFSET + style.offset) + style.offset,
				relx = 0.20,
				relwidth = 0.80,
				height = SIDEBAR_OFFSET,
				width = - 4 * style.offset
			)
			w.set(package["info"][key])
			self.info_entries[key] = w
			self.destroyables.extend([w,w_l])
			i += 1

	def trigger_open_tab(self):
		if self.package:
			try:
				url = self.package["info"]["url"]
				opentab(url)
			except Exception as e:
				print("Failed to open tab - {}".format(e))

	def save_json(self):
		pkg = self.package.copy()

		for key in self.entries.keys():
			pkg[key] = self.entries[key].get_var().get()

		for key in self.info_entries.keys():
			pkg["info"][key] = self.info_entries[key].get_var().get()

		name = pkg["package"]
		print(f"Saving pkgbuild.json for {name}.")
		print(json.dumps(pkg, indent = 4))
		self.appstore_handler.save(name, pkg)
		print(f"Saved pkgbuild.")