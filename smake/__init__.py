import platform
import sys
import os
import errno
import glob

import smake.config

class Smake:
    def __init__(self):
        self.name = ""
        self.obj_dir = "obj"
        self.target = "bin/app"
        self.gcc = smake.config.GccConfig(self)
        self.gcc_cpp = smake.config.GccCppConfig(self)

        self._smake_dir = os.path.join(os.path.expanduser("~"), "smake")
        self._package_dir = os.path.join(self._smake_dir, "packages")
        self._bin_dir = os.path.join(self._smake_dir, "bin")

        self.mkdir_p(self._package_dir)
        self.mkdir_p(self._bin_dir)

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
            if sys.maxsize > 2**32:
                return "linux64"
            else:
                return "linux32"
        elif system == "Darwin":
            return "darwin"

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