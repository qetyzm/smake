import platform
import sys
import os
import errno
import glob

import smake_buildtools.config

class Smake:
    def __init__(self):
        self.name = ""
        self.obj_dir = "obj"
        self.bin_dir = "bin"
        self.gcc = smake_buildtools.config.GccConfig(self)
        self.gcc_cpp = smake_buildtools.config.GccCppConfig(self)
        self.clang = smake_buildtools.config.ClangConfig(self)

        self._smake_dir = os.path.join(os.path.expanduser("~"), "smake")
        self._package_dir = os.path.join(self._smake_dir, "packages")
        self._bin_dir = os.path.join(self._smake_dir, "bin")

        self.mkdir_p(self._package_dir)
        self.mkdir_p(self._bin_dir)

    def _get_target(self):
        return self.bin_dir + os.path.sep + self.name

    def wildcard(self, path):
        return glob.glob(path)

    def merge(self, *path_list):
        lists = []
        for path in path_list:
            lists += path
        return lists
    
    def get_platform(self):
        system = platform.system()
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

    def make_path(self, *path):
        path = list(path)
        for i in range(len(path)):
            if path[i] == "~":
                path[i] = os.path.expanduser(path[i])
        return os.path.join(path)

    def copy_executable_to(self, target_path):
        self.mkdir_p(target_path)
        from shutil import copyfile
        copyfile(self.bin_dir, target_path)

    def remove_dir(self, directory):
        from shutil import rmtree
        rmtree(directory)

    def remove_file(self, file):
        os.remove(file)