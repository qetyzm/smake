class PackageLoader:
    def __load(self):
        pass

    def load(self):
        if not self.exists():
            self.__load()

    def exists(self):
        return False


"""
package: SDL2
"""
class SDL2Loader(PackageLoader):
    def __init__(self, smake):
        self.smake = smake

    def load(self):
        pass

    def exists(self):
        pass