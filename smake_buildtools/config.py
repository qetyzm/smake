import subprocess
import os


class CompilerConfig:
    _compiler = ""

    def __init__(self, smake):
        self.smake = smake

    def available(self):
        from shutil import which
        return which(self._compiler) is not None

    def link(self):
        pass

    def compile(self):
        pass


class GccConfig(CompilerConfig):
    def __init__(self, smake):
        self.smake = smake
        self.sources = []
        self.compiler_flags = []
        self.warning_flags = []
        self.linker_flags = []
        self.include_dirs = []
        self.library_dirs = []
        self._compiler = "gcc"
        self._exit_code = 0
    
    def compile(self):
        print("[SMAKE]\tCompiling...")
        for file in self.sources:
            compiler_flags = " ".join(list(map(
                lambda x: "-" + x, self.compiler_flags)))
            warning_flags = " ".join(list(map(
                lambda x: "-W" + x, self.warning_flags)))
            include_dirs = " ".join(list(map(
                lambda x: "-I" + x, self.include_dirs)))
            linker_flags = " ".join(list(map(
                lambda x: "-l" + x, self.linker_flags)))
            library_dirs = " ".join(list(map(
                lambda x: "-L" + x, self.library_dirs)))

            basename = ".".join(file.split('.')[:-1])
            new_file = self.smake.obj_dir + os.path.sep + basename + ".o"
            self.smake.mkdir_p(
                os.path.sep.join(
                    new_file.split(os.path.sep)[:-1]))
            
            if os.path.exists(new_file):
                continue

            process = "{} -c {} -o {} {} {} {} {} {}".format(
                self._compiler, file, new_file, compiler_flags, 
                warning_flags, include_dirs, linker_flags, library_dirs)
            process = process.split(' ')
            process = list(filter(None, process))

            print("[CC]\t" + ' '.join(process))

            with subprocess.Popen(process, shell=True) as proc:
                self._exit_code = proc.wait()
                if self._exit_code:
                    print("[SMAKE]\tLinking stopped...")
                    return

    def link(self):
        if self._exit_code:
            return
        print("[SMAKE]\tLinking...")
        self.smake.mkdir_p(self.smake.bin_dir)
        all_files = []
        for file in self.sources:
            basename = ".".join(file.split('.')[:-1])
            new_file = self.smake.obj_dir + os.path.sep + basename + ".o"
            self.smake.mkdir_p(
                os.path.sep.join(
                    new_file.split(os.path.sep)[:-1]))
            all_files.append(new_file)
        
        all_files = " ".join(all_files)

        compiler_flags = " ".join(list(map(
            lambda x: "-" + x, self.compiler_flags)))
        warning_flags = " ".join(list(map(
            lambda x: "-W" + x, self.warning_flags)))
        include_dirs = " ".join(list(map(
            lambda x: "-I" + x, self.include_dirs)))
        linker_flags = " ".join(list(map(
            lambda x: "-l" + x, self.linker_flags)))
        library_dirs = " ".join(list(map(
            lambda x: "-L" + x, self.library_dirs)))

        target = self.smake._get_target()

        process = "{} {} -o {} {} {} {} {} {}".format(
            self._compiler, all_files, target, compiler_flags, 
            warning_flags, include_dirs, linker_flags, library_dirs)
        process = process.split(' ')
        process = list(filter(None, process))

        print("[CC]\t" + ' '.join(process))

        with subprocess.Popen(process, shell=True) as proc:
            proc.communicate()


class GccCppConfig(GccConfig):
    def __init__(self, smake):
        super().__init__(smake)
        self._compiler = "g++"


class ClangConfig(GccConfig):
    def __init__(self, smake):
        super().__init__(smake)
        self._compiler = "clang"
