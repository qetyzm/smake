import smake

if __name__ == "__main__":
    sm = smake.Smake()
    sm.name = "app"
    sm.gcc.sources = sm.merge(
        sm.wildcard("src/*.c"), 
        sm.wildcard("src/module_1/*.c"), 
        sm.wildcard("src/module_2/*.c"))
    sm.gcc.warning_flags = ["all", "extra"]
    sm.gcc.compiler_options = ["pedantic", "std=c11"]

    sm.linker_flags = ["sdl2"]
    sm.include_dirs = ["C:\\SDL2\\include"]
    sm.library_dirs = ["C:\\SDL2\\lib"]

    sm.gcc.link()
    sm.gcc.compile()

    # post compile stuff
    if sm.get_platform() == "linux" or sm.get_platform() == "darwin":
        target = "/usr/bin/" + sm.name
        sm.copy_executable_to(target)