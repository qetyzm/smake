import smake


class CompilerConfig:
    __compiler = ""
    __files = []

    def available(self):
        from shutil import which
        return which(self.__compiler) is not None

    def link(self):
        pass

    def compile(self):
        pass


class GccConfig(CompilerConfig):
    def __init__(self, smake):
        self.smake = smake
        self.sources = []
        self.compiler_options = []
        self.warning_flags = []
        self.linker_flags = []
        self.include_flags = []
        self.include_dirs = []
        self.library_dirs = []
        self.__compiler = "gcc"


class GccCppConfig(GccConfig):
    def __init__(self, smake):
        super().__init__(self, smake)
        self.__compiler = "g++"