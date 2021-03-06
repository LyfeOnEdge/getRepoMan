from gui.widgets import basePage, themedListbox, themedLabel, themedFrame, searchBox
import platform
import tkinter as tk
from asyncthreader import threader
import style

sort_option_default = "Sort: Default"
sort_option_package_name_ascending = "Name A -> Z"
sort_option_package_name_descending = "Name Z -> A"
sort_option_package_title_ascending = "Title A -> Z"
sort_option_package_title_descending = "Title Z -> A"
sort_option_package_author_ascending = "Author (A->Z)"
sort_option_package_author_descending = "Author (Z->A)"
# sort_option_package_updated_ascending = "Updated (Recent first)"
# sort_option_package_updated_descending = "Updated (Recent last)"

SORT_OPTIONS = [
	sort_option_default,
	sort_option_package_name_ascending,
	sort_option_package_name_descending,
	sort_option_package_title_ascending,
	sort_option_package_title_descending,
	sort_option_package_author_ascending,
	sort_option_package_author_descending,
	# sort_option_package_updated_ascending,
	# sort_option_package_updated_descending
]

SORT_MAP = {
	sort_option_default : None,
	sort_option_package_name_ascending : "package",
	sort_option_package_name_descending : "package-",
	sort_option_package_title_ascending : "title",
	sort_option_package_title_descending : "title-",
	sort_option_package_author_ascending : "author",
	sort_option_package_author_descending : "author-",
	# sort_option_package_updated_ascending : "updated",
	# sort_option_package_updated_descending : "updated-"
}

class Page(basePage.BasePage):
	def __init__(self,
				 app: tk.Tk,
				 container: tk.Frame,
				 plugin,
				 ):
		basePage.BasePage.__init__(self, app, container, "getRepoMan")
		# assert len(category_packages) != 0,"No packages!"
		self.packages = []
		self.current_search = None
		self.selected = False
		self.sort_type = None
		self.listbox_list = []
		self.picked = False
		self.last_sort_option = None
		self.plugin = plugin
		self.handler = plugin.handler
		self.handler.set_reload_function(self.set_packages)

		self.build_listframe()

	def set_packages(self, packages):
		self.packages = packages
		self.rebuild()

	def build_listframe(self):
		self.header = tk.Frame(self, background = style.primary_color)

		self.header = themedFrame.ThemedFrame(self)
		self.header.place(relx = 0, rely = 0, relwidth = 1, height = style.searchboxheight)

		self.content_frame_header_search_bar = searchBox.SearchBox(self.header, command = self.search, entry_background=style.secondary_color, borderwidth = 0, entry_foreground = style.primary_text_color)

		self.selected_sort_method = tk.StringVar()
		self.selected_sort_method.set(SORT_OPTIONS[0])
		self.content_frame_header_sort_method_dropdown = tk.OptionMenu(self.header,self.selected_sort_method,*SORT_OPTIONS)
		self.content_frame_header_sort_method_dropdown.configure(foreground = style.primary_text_color)
		self.content_frame_header_sort_method_dropdown.configure(background = style.secondary_color)
		self.content_frame_header_sort_method_dropdown.configure(highlightthickness = 0)
		self.content_frame_header_sort_method_dropdown.configure(borderwidth = 0)

		self.content_frame_header_sort_method_dropdown.place(relx = 1, x = -(style.offset + style.sortdropdownwidth), width = style.sortdropdownwidth, y=+ 1.5 * style.offset, relheight =1, height = - 2 *style.offset)
		self.content_frame_header_sort_method_dropdown.unbind("<F10>")
		self.content_frame_header_search_bar.place(x = 0, y=+ 1.5 * style.offset, relheight =1, relwidth = 1, width = - (2 * style.offset + style.sortdropdownwidth), height = - 2 *style.offset)

		self.body_frame = tk.Frame(self, background = style.primary_color)
		self.body_frame.place(y = style.searchboxheight, height = - style.searchboxheight, relwidth = 1, relheight = 1)
		self.scrollbar = tk.Scrollbar(self.body_frame, troughcolor = style.primary_color, bg = style.secondary_color)
		self.scrollbar.place(relheight = 1, width = style.scrollbarwidth, relx = 1, x = -style.scrollbarwidth, height = - (style.listbox_footer_height), y = + style.listbox_header_height)
		self.listbox_frame = tk.Frame(self.body_frame, background = style.secondary_color)
		self.listbox_frame.place(relwidth = 1, relheight = 1,width = -style.scrollbarwidth)
		self.scaling_listboxes_frame = tk.Frame(self.listbox_frame, background = style.secondary_color)
		self.scaling_listboxes_frame.place(relwidth = 1, relheight = 1)
		self.scaling_listboxes_frame_header = tk.Frame(self.scaling_listboxes_frame, background = style.secondary_color)
		self.scaling_listboxes_frame_header.place(relwidth = 1, height = style.listbox_header_height)
		self.scaling_listboxes_frame_body = tk.Frame(self.scaling_listboxes_frame, background = style.secondary_color)
		self.scaling_listboxes_frame_body.place(relwidth = 1, relheight = 1, y = style.listbox_header_height, height = -style.listbox_header_height)
		self.package_listbox = themedListbox.ThemedListbox(self.scaling_listboxes_frame_body, background = style.secondary_color,font = style.smallboldtext, borderwidth = 1, foreground = style.primary_text_color)
		self.package_listbox.place(relx = 0, relwidth = 0.33333, relheight = 1)
		self.package_listbox_label = themedLabel.ThemedLabel(self.scaling_listboxes_frame_header, text = "Package", background = style.primary_color, font = style.mediumboldtext)
		self.package_listbox_label.place(relx = 0, relwidth = 0.33333, relheight = 1)
		self.title_listbox = themedListbox.ThemedListbox(self.scaling_listboxes_frame_body, background = style.secondary_color,font = style.smalltext, borderwidth = 1)
		self.title_listbox.place(relx = 0.33333, relwidth = 0.33333, relheight = 1)
		self.title_listbox_label = themedLabel.ThemedLabel(self.scaling_listboxes_frame_header, text = "Title", background = style.primary_color, font = style.mediumboldtext)
		self.title_listbox_label.place(relx = 0.33333, relwidth = 0.33333, relheight = 1)
		self.author_listbox = themedListbox.ThemedListbox(self.scaling_listboxes_frame_body, background = style.secondary_color,font = style.smalltext, borderwidth = 1)
		self.author_listbox.place(relx = 0.66666, relwidth = 0.33333, relheight = 1)
		self.author_listbox_label = themedLabel.ThemedLabel(self.scaling_listboxes_frame_header, text = "Author", background = style.primary_color, font = style.mediumboldtext)
		self.author_listbox_label.place(relx = 0.66666, relwidth = 0.33333, relheight = 1)
		self.listbox_list = [
			self.package_listbox,
			self.title_listbox,
			self.author_listbox,
		]
		self.package_listbox.configure({"selectbackground" : style.lg})
		self.package_listbox.configure({"selectmode" : "single"})
		self.package_listbox.bind("<<ListboxSelect>>", self.on_listbox_selection)

		self.scrollbar.config(command=self.on_scroll_bar)
		self.package_listbox.config(yscrollcommand=self.scrollbar.set)      

		bindlist = [
			self,
			self.package_listbox,
			self.title_listbox,
			self.author_listbox,
		]

		if platform.system() == 'Windows' or platform.system() == "Darwin":
			for b in bindlist:
				b.bind("<MouseWheel>", self.on_mouse_wheel)
		elif platform.system() == "Linux":
			for b in bindlist:
				b.bind("<Button-4>", self.on_mouse_wheel)
				b.bind("<Button-5>", self.on_mouse_wheel)   

		self.set_sort_type(None)
		self.rebuild()
		self.sort_check_loop()

	def get_current_packages(self):
		packages = self.search_packages(self.current_search)
		if self.sort_type:
			packages = self.sort_packages(packages, self.sort_type)
		return packages

	def configure(self, event = None, force = False):
		self.handler.set_path(self.app.path)
		if self.picked or force:
			self.rebuild()

	def search_packages(self, search: str = ""):
		def do_search(package):
			for field in ["package", "changelog"]:
				if search.lower() in package[field].lower():
					return package
					
			for field in ["author", "name", "title", "description"]:
				if search.lower() in package["info"][field].lower():
					return package

			for asset in package["assets"]:
				for item in asset.keys():
					if search.lower() in item.lower():
						return package
					if search.lower() in asset[item].lower():
						return package

		if search:
			packages = []
			for package in self.packages:
				try:
					result = do_search(package)
					if result:
						packages.append(package)
				except:
					pass
			return packages if packages else [{"package" : "NO RESULTS", "info" : {"title" : "", "author" : "", "updated" : ""}}]
		else:
			return self.packages

	def on_listbox_selection(self, event):
		selection=self.package_listbox.curselection()
		picked = self.package_listbox.get(selection[0])
		for package in self.packages:
			if package["package"] == picked:
				self.open_details(package)

	def sort_packages(self, packages, sort_method):
		reverse = False
		if sort_method.endswith('-'):
			reverse = True
			sort_method = sort_method.strip('-')

		return sorted(packages, key=lambda k: k["info"][sort_method], reverse = reverse)

	def rebuild(self):
		self.build_frame(self.get_current_packages())
	
	def build_frame(self, packages):
		if not packages:
			print("No packages to build with")
			return

		self.clear()

		self.listbox_list = [
			self.package_listbox,
			self.title_listbox,
			self.author_listbox,
		]

		if self.listbox_list:
			for lb in self.listbox_list:
				lb.configure(state = "normal")

			for package in packages:
				if not package:
					continue

				self.package_listbox.insert('end', package["package"])
				self.title_listbox.insert('end', package["info"]["title"])
				self.author_listbox.insert('end', package["info"]["author"])

			for lb in self.listbox_list:
				lb.configure(state = "disable")
			self.package_listbox.configure(state = 'normal')

	def select(self):
		self.selected = True

	def deselect(self):
		self.selected = False

	def is_selected(self):
		return self.selected

	def search(self, searchterm):
		self.current_search = searchterm
		self.rebuild()

	def clear(self):
		if self.listbox_list:
			for lb in self.listbox_list:
				lb.configure(state = "normal")
				lb.delete(0, "end")
				lb.configure(state = "disable")

	def on_scroll_bar(self, move_type, move_units, __ = None):
		if move_type == "moveto":
			for lb in self.listbox_list:
				lb.yview_moveto(move_units)

	def on_mouse_wheel(self, event):
		try:
			if platform.system() == 'Windows':
				self.package_listbox.yview("scroll", int(-1*(event.delta/120),"units"))
			elif platform.system() == "Linux":
				if event.num == 5:
					self.package_listbox.yview("scroll", 1,"units")
				if event.num == 4:
					self.package_listbox.yview("scroll", -1,"units")
			elif platform.system() == "Darwin":
				self.package_listbox.yview("scroll", event.delta,"units")

			for lb in self.listbox_list:
				lb.yview_moveto(self.package_listbox.yview()[0])

			return "break"
		except:
			pass

	def set_sort_type(self, sort_type):
		self.sort_type = sort_type

	#loop to check if the sorting method has been applied yet
	def sort_check_loop(self):
		if not self.last_sort_option == self.selected_sort_method.get():
			self.last_sort_option = self.selected_sort_method.get()
			self.update_sort()
			self.rebuild()

		#schedule self
		self.app.after(100, self.sort_check_loop)

	def update_sort(self):
		self.set_sort_type(SORT_MAP[self.selected_sort_method.get()])


	def open_details(self, package):
		self.plugin.detail_page.show(package, self.handler)