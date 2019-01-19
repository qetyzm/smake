import platform
import sys
import os
import errno
import glob

import smake.configs
import smake.package_loaders


class Smake:
    def __init__(self):
        self.name = ""
        self.lang = ""
        self.obj_dir = "obj"
        self.target = "bin/app"
        self.gcc = smake.configs.GccConfig(self)
        self.gplusplus = smake.configs.GccCppConfig(self)
        self.__loaders = {
            "sdl2": smake.package_loaders.SDL2Loader(self)
        }

        self.__smake_dir = os.path.join(os.path.expanduser("~"), "smake")
        self.__package_dir = os.path.join(self.__smake_dir, "packages")
        self.__bin_dir = os.path.join(self.__smake_dir, "bin")

        self.mkdir_p(self.__package_dir)
        self.mkdir_p(self.__bin_dir)

    def wildcard(self, path):
        return glob.glob(path)

    def merge(self, *path_list):
        lists = []
        for path in path_list:
            lists += path
        return lists
    
    def get_platform(self):
        system = platform.platform()
        if system == "Windows":
            if sys.maxsize > 2**32:
                return "win64"
            else:
                return "win32"
        elif system == "Linux":
            return "linux"
        elif system == "Darwin":
            return "darwin"

    def load_package(self, package_name):
        package_name = package_name.lower().strip()
        if package_name in self.__loaders.keys():
            self.__loaders[package_name].load()

    def package_exists(self, package_name):
        package_name = package_name.lower().strip()
        if package_name in self.__loaders.keys():
            return self.__loaders[package_name].exists()

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
        
    def copy_executable_to(self, target_path):
        self.mkdir_p(target_path)
        from shutil import copyfile
        copyfile(self.target, target_path)