import smake

sm = Smake()
sm.name = "app"
sm.lang = "C"
sm.gcc.sources = ["src/*.c", "src/module_1/*.c", "src/module_2/*.c"]
sm.gcc.compiler_options = "-Wall -pedantic"
sm.gcc.target = "build/" + sm.get_platform()
sm.gcc.obj_dir = "obj"
sm.gcc.load_package("sdl2")

# sm.load_package() has SDL2 in repository so it will automatically set all the flags
#sm.linker_flags = ["sdl2"]
#sm.include_flags = []
#sm.include_dirs = ["C:\\SDL2\\include"]
#sm.library_dirs = ["C:\\SDL2\\lib"]

if __name__ == "__main__":
    sm.gcc.compile()

    # post compile stuff
    if sm.get_platform() == "linux":
        target = "/usr/bin/" + sm.name
        sm.copy_executable_to(target)