import os, sys, shutil, json

ICON  = "icon.png"
SCREEN = "screen.png"

class RepoHandler(object):
    def __init__(self):
        self.selected_path = None
        self.packages = None
        self.reload_function = None
        self.repo = []

    #Set this to the path you want to work on
    def set_path(self, path: str):
        self.selected_path = path
        if self.selected_path:
            print(f"Set Repo Manager path to {path}")
        else:
            print("Invalid path set")
        self.packages = None
        self.reload_function(self.get_packages())

    def getPackageIcon(self, package, force = False):
        s = os.path.join(os.path.join(self.selected_path, package), ICON)
        return (s if os.path.isfile(s) else None)

    def getScreenImage(self, package, force = False):
        s = os.path.join(os.path.join(self.selected_path, package), SCREEN)
        return (s if os.path.isfile(s) else None)

    def set_reload_function(self, reload_function):
        self.reload_function = reload_function

    #looks in set path for any folders containing a pkgbuild.json 
    #loads any if finds and adds the pkgbuild to self.packages
    #Finally returns self.packages
    def get_packages(self, silent: bool = False):
        if not self.check_path():
            return (warn_path_not_set() if not silent else None)

        packages = []
        # Go through items in packages dir
        for possible_package in os.listdir(self.selected_path):
            # Find the path of the package
            package_dir = os.path.join(self.selected_path, possible_package)
            package_json = os.path.join(package_dir, "pkgbuild.json")
            # check if the json exists (isfile will result in exception if
            # it doesn't exist, it's unlikely to find a folder named
            # info.json, either way exists() will have to be called)
            if os.path.exists(package_json):
                try:
                    with open(package_json) as pkg:
                        packages.append(json.load(pkg))
                except Exception as e:
                    print(f"Failed to load pkgbuild for {packake_dir}")

        print(f"Found {len(packages)} libget metadata entries (pkgbuild.json)")
        # print("Found packages -\n{}".format(json.dumps(packages, indent=4)))
        self.packages = packages
        return self.packages

    def reload(self):
        self.set_path(self.selected_path)

    def check_path(self):
        return self.selected_path

    # Get the contents of a package's info file as a dict
    # Returns none if it doesn't exist
    # def get_package_entry(self, package_name: str):
    #     if not self.check_path():
    #         return

    #     packagedir = os.path.join(self.selected_path, package_name)
    #     pkg = os.path.join(packagedir, "pkgbuild.json")

    #     try:
    #         with open(pkg, encoding="utf-8") as infojson:
    #             return json.load(infojson)
    #     except FileNotFoundError:
    #         pass
    #     except Exception as e:
    #         print(f"Failed to open pkgbuild data for {package_name} - {e}")

    # # Get a package's json file value, returns none if it fails
    # def get_package_value(self, package_name: str, key: str):
    #     if not self.check_path():
    #         return
    #     # Get the package json data
    #     package_info = self.get_package_entry(package_name)
    #     # If data was retrieved, return the value
    #     if package_info:
    #         return package_info[key]

    # # Get the installed version of a package
    # def get_package_version(self, package_name: str):
    #     return self.get_package_value(package_name, "version")

   
    # def edit_info(self, package_name: str, key: str, value):
    #     if not self.check_path():
    #         return warn_path_not_set()
    #     packagedir = os.path.join(self.selected_path, self.libget_dir)
    #     packagesdir = os.path.join(self.selected_path, self.libget_dir)
    #     packagedir = os.path.join(packagesdir, package_name)
    #     pkg = os.path.join(packagedir, PACKAGE_INFO)

    #     try:
    #         with open(pkg, encoding="utf-8") as infojson:
    #             info = json.load(infojson)
    #     except Exception as e:
    #         print(f"Failed to open info data for {package_name} - {e}")
    #         return

    #     info[key] = value

    #     with open(pkg, "w", encoding="utf-8") as infojson:
    #         json.dump(info, infojson)

    #     return True

    def clean_version(self, ver, name):
        ver = ver.lower().strip("v")
        if name:
            ver = ver.replace(name.lower(), "")
        ver = ver.split(" ")[0].replace("switch", "").strip("-")
        return ver

    def save(self, package_name: str, pkgbuild: dict):
        package_dir = os.path.join(self.selected_path, package_name)
        package_json = os.path.join(package_dir, "pkgbuild.json")
        with open(package_json, "w+") as p:
            json.dump(pkgbuild, p, indent = 2)

def warn_path_not_set():
    print("Warning: Repo Manager path not set")